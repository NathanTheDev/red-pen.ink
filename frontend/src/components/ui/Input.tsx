export function Input({ label = "Input", placeholder = "Type here..." }) {
  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className="text-sm font-bold text-[#A89880] mb-2">{label}</p>
        <input
          type="text"
          placeholder={placeholder}
          className="w-full py-3 px-6 rounded-full border border-[#4A3E30] bg-[#3D3328] shadow-sm text-sm text-[#A89880] placeholder:text-[#6B5C4A] focus:outline-none focus:ring-1 focus:ring-[#4A3E30] transition-colors hover:bg-[#45392D]"
        />
      </div>
    </div>
  );
}
