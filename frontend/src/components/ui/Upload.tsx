import { useState } from "react";

export function Upload({
  label = "File Upload",
  content = "Upload a file...",
  multiple = false,
}) {
  const [fileNames, setFileNames] = useState<string[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? []);
    setFileNames(files.map((f) => f.name));
  };

  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className="text-sm font-bold text-[#A89880] mb-2">{label}</p>
        <label className="flex items-center justify-center gap-3 w-full py-3 px-6 rounded-full border border-[#4A3E30] bg-[#3D3328] shadow-sm text-sm text-[#A89880] cursor-pointer hover:bg-[#45392D] transition-colors">
          <span>
            {fileNames.length === 0
              ? content
              : fileNames.length === 1
                ? fileNames[0]
                : `${fileNames.length} files selected`}
          </span>
          <input
            type="file"
            accept=".docx"
            multiple={multiple}
            onChange={handleChange}
            className="hidden"
          />
        </label>
      </div>
    </div>
  );
}
