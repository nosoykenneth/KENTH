import OllamaChat from '@/features/assistant/components/OllamaChat';
import CoursesCollection from '@/features/courses/components/CoursesCollection';
import CoursesOverviewHeader from '@/features/courses/components/CoursesOverviewHeader';
import useEnrolledCourses from '@/features/courses/hooks/useEnrolledCourses';
import { getMoodleFullName } from '@/shared/lib/moodleSession';

export default function CoursesDashboardPage() {
  const { courses, error, isLoading } = useEnrolledCourses();
  const fullName = getMoodleFullName() || 'Estudiante';

  return (
    <div className="flex flex-col gap-8">
      <CoursesOverviewHeader
        courseCount={courses.length}
        fullName={fullName}
        isLoading={isLoading}
      />

      <section className="flex flex-col gap-5">
        <div className="flex items-end justify-between gap-4 flex-wrap">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-gray-500 font-black mb-2">
              Catalogo
            </p>
            <h2 className="text-2xl md:text-3xl font-black uppercase tracking-tight text-white">
              Tus clases
            </h2>
          </div>
          <p className="text-sm text-gray-400 max-w-xl">
            El grid de cursos ahora vive en componentes separados para que puedas
            cambiar estados, tarjetas o filtros sin tocar el resto del dashboard.
          </p>
        </div>

        <CoursesCollection courses={courses} error={error} isLoading={isLoading} />
      </section>

      <section className="flex flex-col gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500 font-black mb-2">
            Asistente
          </p>
          <h2 className="text-2xl md:text-3xl font-black uppercase tracking-tight text-white">
            Ayuda contextual
          </h2>
        </div>
        <OllamaChat />
      </section>
    </div>
  );
}
