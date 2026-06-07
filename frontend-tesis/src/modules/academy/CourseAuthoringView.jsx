import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { listAxes } from '../../shared/services/axesService';
import { showNotification } from '../../shared/components/ui/Notification';
import PageContainer from '../../shared/components/layout/PageContainer';
import KnowledgeHub from './KnowledgeHub';
import StructureManager from './StructureManager';

/**
 * CourseAuthoringView — "Gestión del tutor"
 *
 * Centro de mando del contenido del tutor, en dos pestañas:
 *  - ESTRUCTURA: temario (ejes → lecciones). Crear/editar/ordenar.
 *  - CONOCIMIENTO: documentos RAG del curso (DocumentManager).
 *
 * El detalle de cada lección (bloques/transcripción) se edita en el editor sobre
 * el video, desde "Enlazar lección" en el recurso H5P dentro del curso.
 */

const TABS = [
  { id: 'estructura', label: 'Estructura' },
  { id: 'conocimiento', label: 'Conocimiento' },
];

export default function CourseAuthoringView() {
  const { courseId } = useParams(); // id firmado del curso (X-Course-Id)
  const [tab, setTab] = useState('estructura');
  const [axes, setAxes] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAxes = useCallback(async () => {
    try {
      setAxes(await listAxes(courseId));
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => { loadAxes(); }, [loadAxes]);

  return (
    <PageContainer>
      <div className="mb-4">
        <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Autoría del curso</p>
        <h1 className="text-2xl font-black uppercase italic text-kenth-text tracking-tight">Gestión del tutor</h1>
        <p className="text-xs text-kenth-subtext mt-1">
          Administra el temario (ejes y lecciones) y el conocimiento (RAG) del curso.
        </p>
      </div>

      <div className="flex border-b border-kenth-border mb-5">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`px-4 py-2.5 text-[11px] font-black uppercase tracking-widest transition ${
              tab === t.id ? 'text-kenth-brightred border-b-2 border-kenth-brightred' : 'text-kenth-subtext hover:text-kenth-text'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-sm text-kenth-subtext">Cargando…</p>
      ) : tab === 'estructura' ? (
        <StructureManager courseId={courseId} />
      ) : (
        <KnowledgeHub courseId={courseId} axes={axes} />
      )}
    </PageContainer>
  );
}
