export function Sidebar() {
  return (
    <div className="flex flex-col w-56 h-screen bg-[#FAF0D7] px-4 py-8 gap-2">
      <span className="text-xs font-semibold text-[#A0896A] uppercase tracking-widest mb-2">
        Modules
      </span>
      <button className="text-left px-3 py-2 rounded-lg text-[#7C5C3A] text-sm font-medium hover:bg-[#F0E0C0] transition-colors cursor-pointer">
        Module A & B
      </button>
      <button className="text-left px-3 py-2 rounded-lg text-[#7C5C3A] text-sm font-medium hover:bg-[#F0E0C0] transition-colors cursor-pointer">
        Module C
      </button>
    </div>
  );
}
