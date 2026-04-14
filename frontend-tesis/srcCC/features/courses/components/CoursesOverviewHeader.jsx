export default function CoursesOverviewHeader({ courseCount, fullName, isLoading }) {
  const counterLabel = isLoading
    ? 'Sincronizando'
    : `${courseCount} ${courseCount === 1 ? 'clase activa' : 'clases activas'}`;

  return (
    <section className="relative overflow-hidden rounded-[2rem] border border-kenth-surface/20 bg-[#1e1e20] p-8 lg:p-10">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-14 right-0 w-56 h-56 rounded-full bg-kenth-brightred/10 blur-[110px]" />
        <div className="absolute -bottom-20 left-12 w-40 h-40 rounded-full bg-white/5 blur-[90px]" />
      </div>

      <div className="relative z-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.35em] text-kenth-brightred font-black mb-3">
            Clases
          </p>
          <h1 className="text-3xl md:text-5xl font-black uppercase tracking-tight text-white">
            Hola, {fullName}
          </h1>
          <p className="mt-4 text-gray-400 max-w-2xl leading-relaxed">
            El catalogo quedo desacoplado por feature para que puedas cambiar tarjetas,
            estados, asistentes y futuras vistas de cursos sin tocar toda la pantalla.
          </p>
        </div>

        <div className="flex flex-wrap gap-3 lg:justify-end">
          <div className="min-w-44 rounded-2xl border border-white/8 bg-white/5 px-5 py-4">
            <p className="text-[11px] uppercase tracking-[0.3em] text-gray-500 font-black mb-2">
              Estado
            </p>
            <p className="text-white font-semibold">{counterLabel}</p>
          </div>
          <div className="min-w-44 rounded-2xl border border-white/8 bg-white/5 px-5 py-4">
            <p className="text-[11px] uppercase tracking-[0.3em] text-gray-500 font-black mb-2">
              Escala
            </p>
            <p className="text-white font-semibold">UI separada por modulo</p>
          </div>
        </div>
      </div>
    </section>
  );
}
