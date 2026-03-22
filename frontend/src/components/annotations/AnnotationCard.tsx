type AnnotationCardProps = {
  annotation: { span: string; comment: string };
  index: number;
  isActive: boolean;
  position: number;
  onClick: () => void;
  dark: boolean;
};

export function AnnotationCard({
  annotation,
  index,
  isActive,
  position,
  onClick,
  dark,
}: AnnotationCardProps) {
  return (
    <div
      onClick={onClick}
      className="absolute cursor-pointer transition-all duration-200"
      style={{
        top: position ?? 0,
        left: "calc(100% + 16px)",
        width: "220px",
        zIndex: isActive ? 10 : 1,
      }}
    >
      <div
        className={`rounded-2xl border px-4 py-3 transition-all duration-200 ${
          isActive
            ? dark
              ? "border-red-500/50 bg-[#2E1A1A] shadow-lg shadow-red-900/20"
              : "border-red-300 bg-red-50 shadow-lg shadow-red-100"
            : dark
              ? "border-[#2E2820] bg-[#252019] opacity-60 hover:opacity-100"
              : "border-[#E2D9CE] bg-white opacity-60 hover:opacity-100"
        }`}
      >
        <p className="text-red-400 font-mono text-xs mb-1 truncate">
          "{annotation.span}"
        </p>
        <p className={`text-xs leading-relaxed ${dark ? "text-[#A89880]" : "text-[#6B5744]"}`}>
          {annotation.comment}
        </p>
      </div>
    </div>
  );
}