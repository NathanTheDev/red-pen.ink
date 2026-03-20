import logo from "@assets/pen-icon.png";

export function Upload() {
  return (
    <div className="flex flex-col items-center gap-6 pt-16">
      {/* Title row */}
      <div className="flex items-center gap-3">
        <img src={logo} alt="Red.ink logo" className="w-10 h-10" />
        <h1 className="text-4xl font-bold tracking-tight text-red-500">
          Red.ink
        </h1>
      </div>

      {/* File upload */}
      <div className="relative w-full max-w-xl">
        <label className="flex items-center justify-center gap-3 w-full py-3 px-6 rounded-full border border-neutral-200 bg-white shadow-sm text-sm text-neutral-400 cursor-pointer hover:bg-neutral-50 transition-colors">
          <span>Upload a file...</span>
          <input type="file" className="hidden" />
        </label>
      </div>
    </div>
  );
}
