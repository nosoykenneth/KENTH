import React, { useState, useCallback, useRef } from 'react';
import Cropper from 'react-easy-crop';
import { motion } from 'framer-motion';
import { getCroppedImg } from '../../utils/cropImage';

const CROP_SIZE = { width: 250, height: 250 };
const EDGE_TOLERANCE = 2;

const COLOR_VARIANTS = {
  indigo: {
    label: 'text-indigo-400',
    range: 'accent-indigo-500',
    confirm: 'bg-indigo-600 hover:bg-indigo-500 shadow-[0_10px_30px_rgba(79,70,229,0.4)]',
    cropBorder: 'rgba(255, 255, 255, 0.4)',
  },
  brand: {
    label: 'text-kenth-brightred',
    range: 'accent-kenth-brightred',
    confirm: 'bg-kenth-brightred hover:bg-kenth-red shadow-[0_10px_30px_rgba(195,7,63,0.35)]',
    cropBorder: 'rgba(195, 7, 63, 0.65)',
  },
};

export default function AvatarCropper({
  image,
  onCropComplete,
  onCancel,
  variant = 'indigo',
  initialCropState = null,
}) {
  const containerRef = useRef(null);
  const colors = COLOR_VARIANTS[variant] || COLOR_VARIANTS.indigo;

  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [baseZoom, setBaseZoom] = useState(1);
  const [croppedArea, setCroppedArea] = useState(null);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);

  const onMediaLoaded = useCallback((mediaSize) => {
    const container = containerRef.current;
    if (!container) return;

    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    if (!containerWidth || !containerHeight) return;

    const containZoom = Math.min(
      containerWidth / mediaSize.width,
      containerHeight / mediaSize.height
    );

    const coverCropZoom = Math.max(
      (CROP_SIZE.width + EDGE_TOLERANCE) / mediaSize.width,
      (CROP_SIZE.height + EDGE_TOLERANCE) / mediaSize.height
    );

    const initialZoom = Math.max(1, containZoom, coverCropZoom);
    const restoredArea = initialCropState?.areaPercentages;
    const restoredZoom = restoredArea?.width && restoredArea?.height
      ? Math.max(
          CROP_SIZE.width / (mediaSize.width * (restoredArea.width / 100)),
          CROP_SIZE.height / (mediaSize.height * (restoredArea.height / 100))
        )
      : initialZoom;
    const nextZoom = Math.min(Math.max(initialZoom, restoredZoom), initialZoom * 4);

    setBaseZoom(initialZoom);
    setZoom(nextZoom);
    if (!restoredArea) {
      setCrop({ x: 0, y: 0 });
    }
  }, [initialCropState]);

  const onCropAreaComplete = useCallback((croppedArea, croppedAreaPixels) => {
    setCroppedArea(croppedArea);
    setCroppedAreaPixels(croppedAreaPixels);
  }, []);

  const handleDone = async () => {
    try {
      if (!croppedAreaPixels) return;

      const croppedImage = await getCroppedImg(image, croppedAreaPixels);
      onCropComplete(croppedImage, {
        areaPercentages: croppedArea,
        areaPixels: croppedAreaPixels,
      });
    } catch (e) {
      console.error(e);
    }
  };

  const zoomPercent = Math.round((zoom / baseZoom) * 100);

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/85 backdrop-blur-2xl animate-in fade-in duration-500">
      <div className="relative flex flex-col items-center gap-10 w-full max-w-2xl px-6">

        <motion.div
          ref={containerRef}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="relative w-[300px] h-[300px] md:w-[400px] md:h-[400px] overflow-hidden border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] bg-[#050505]"
        >
          <Cropper
            image={image}
            crop={crop}
            zoom={zoom}
            minZoom={baseZoom}
            maxZoom={baseZoom * 4}
            aspect={1}
            cropShape="round"
            showGrid={false}
            cropSize={CROP_SIZE}
            initialCroppedAreaPercentages={initialCropState?.areaPercentages}
            objectFit="contain"
            restrictPosition={true}
            onMediaLoaded={onMediaLoaded}
            onCropChange={setCrop}
            onZoomChange={setZoom}
            onCropComplete={onCropAreaComplete}
            style={{
              containerStyle: {
                width: '100%',
                height: '100%',
              },
              cropAreaStyle: {
                border: `2px solid ${colors.cropBorder}`,
                boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.75)',
              },
            }}
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="w-full flex flex-col items-center gap-8"
        >
          <div className="w-full max-w-[260px] flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <span className="text-[9px] font-black uppercase tracking-[0.3em] text-white/30 italic">
                Zoom de Identidad
              </span>

              <span className={`text-[9px] font-black tracking-widest ${colors.label}`}>
                {zoomPercent}%
              </span>
            </div>

            <input
              type="range"
              value={zoom}
              min={baseZoom}
              max={baseZoom * 4}
              step={0.01}
              onChange={(e) => setZoom(Number(e.target.value))}
              className={`w-full h-1 bg-white/10 rounded-full appearance-none cursor-pointer ${colors.range}`}
            />
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={onCancel}
              className="px-6 py-2.5 rounded-xl bg-white/5 text-white/40 font-bold text-[9px] uppercase tracking-widest hover:bg-white/10 hover:text-white transition-all active:scale-95"
            >
              Cancelar
            </button>

            <button
              onClick={handleDone}
              className={`px-10 py-3 rounded-xl text-white font-black text-[9px] uppercase tracking-widest transition-all active:scale-95 ${colors.confirm}`}
            >
              Confirmar
            </button>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
