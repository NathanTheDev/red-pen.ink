interface InputProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function Input({ label = "Input", placeholder = "Type here...", value, onChange }: InputProps) {
  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className="text-sm font-bold text-[#A89880] mb-2">{label}</p>
        <input
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="w-full py-3 px-6 rounded-full border border-[#4A3E30] bg-[#3D3328] text-sm text-[#D4C4A8] placeholder:text-[#6B5C4A] focus:outline-none focus:ring-1 focus:ring-[#4A3E30] transition-colors hover:bg-[#45392D]"
        />
      </div>
    </div>
  );
}