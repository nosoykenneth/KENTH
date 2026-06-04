import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { listAxes } from '../../shared/services/axesService';
import { showNotification } from '../../shared/components/ui/Notification';
import PageContainer from '../../shared/components/layout/PageContainer';
import DocumentManager from './DocumentManager';

/**
 * CourseAuthoringView — "Gestión del tutor"
 *
 * Tras el rediseño, esta vista queda enfocada SOLO en los documentos de
 * conocimiento (RAG) del curso. La edición de lecciones, bloques de video y
 * prompts se movió al editor visual sobre el video (LessonVideoEditor), que se
 * abre desde "Enlazar lección" en el recurso H5P dentro del curso.
 */
export default function CourseAuthoringView() {
  const { courseId } = useParams(); // id firmado del curso (X-Course-Id)
  const [axes, setAxes] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAxes = useCallback(async () => {
    try {
      const data = await listAxes(courseId);
      setAxes(data);
    } catch (e) {
      showNotification('error', e.message);
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => { loadAxes(); }, [loadAxes]);

  return (
    <PageContainer>
      <div className="mb-5">
        <p className="text-[10px] uppercase font-black tracking-widest text-kenth-brightred">Autoría del curso</p>
        <h1 className="text-2xl font-black uppercase italic text-kenth-text tracking-tight">Gestión del tutor</h1>
        <p className="text-xs text-kenth-subtext mt-1">
          Sube y administra el conocimiento (RAG) del curso. Para editar lecciones, bloques de video y
          prompts del tutor, abre un recurso H5P del curso y usa <span className="text-kenth-text font-bold">Enlazar lección</span>.
        </p>
      </div>

      {loading ? (
        <p className="text-sm text-kenth-subtext">Cargando…</p>
      ) : (
        <DocumentManager courseId={courseId} axes={axes} />
      )}
    </PageContainer>
  );
}
