export function Input({
  label = "Input",
  placeholder = "Type here...",
}) {
  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className="text-sm font-bold text-[#5C3D1E] mb-2">{label}</p>
        <input
          type="text"
          placeholder={placeholder}
          className="w-full py-3 px-6 rounded-full border border-neutral-200 bg-white shadow-sm text-sm text-neutral-400 placeholder:text-neutral-400 focus:outline-none focus:ring-1 focus:ring-neutral-300 transition-colors hover:bg-neutral-50"
        />
      </div>
    </div>
  );
}