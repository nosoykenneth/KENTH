import CourseCard from '@/features/courses/components/CourseCard';

export default function CoursesCollection({ courses, error, isLoading }) {
  if (isLoading) {
    return (
      <div className="bg-[#2D2D30] rounded-[2rem] p-12 lg:p-16 border border-kenth-surface/20 flex justify-center items-center">
        <svg className="animate-spin h-10 w-10 text-kenth-brightred" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border-l-4 border-kenth-brightred p-6 rounded-r-xl">
        <p className="text-red-200 font-bold font-sans">Ha ocurrido un problema: {error}</p>
      </div>
    );
  }

  if (!courses.length) {
    return (
      <div className="bg-[#2D2D30] rounded-[2rem] p-8 lg:p-12 border border-kenth-surface/20 shadow-lg text-center opacity-80 border-dashed">
        <h3 className="text-gray-300 font-bold mb-2">Aun no estas matriculado en ningun curso.</h3>
        <p className="text-gray-500 text-sm">
          Cuando aparezcan nuevas clases, esta seccion podra crecer sin tocar el resto del dashboard.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 relative z-10">
      {courses.map((course, index) => (
        <CourseCard key={course.id} curso={course} index={index} btnText="Entrar" themeScheme="red" />
      ))}
    </div>
  );
}
