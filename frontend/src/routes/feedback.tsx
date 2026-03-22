import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Title } from "@/components/ui/Title";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { useTheme } from "@/context/ThemeContext";
import { zodValidator } from "@tanstack/zod-adapter";
import { z } from "zod";
import { useRef, useState, useEffect } from "react";
import { buildSegments } from "@/lib/feedback";

const feedbackSearchSchema = z.object({
  userId: z.string(),
  annotations: z.array(z.object({ span: z.string(), comment: z.string() })),
  content: z.string(),
});

export const Route = createFileRoute("/feedback")({
  validateSearch: zodValidator(feedbackSearchSchema),
  component: FeedbackComponent,
});

function FeedbackComponent() {
  const navigate = useNavigate();
  const { annotations, userId, content } = Route.useSearch();
  const { theme } = useTheme();
  const dark = theme === "dark";

  const spanRefs = useRef<(HTMLElement | null)[]>([]);
  const [positions, setPositions] = useState<number[]>([]);
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  const segments = buildSegments(content, annotations);

  useEffect(() => {
    const updatePositions = () => {
      const containerTop = contentRef.current?.getBoundingClientRect().top ?? 0;
      const tops = spanRefs.current.map((el) => {
        if (!el) return 0;
        return el.getBoundingClientRect().top - containerTop;
      });
      setPositions(tops);
    };

    updatePositions();
    window.addEventListener("resize", updatePositions);
    return () => window.removeEventListener("resize", updatePositions);
  }, [segments]);

  return (
    <div
      className={`min-h-screen flex flex-col items-center p-8 transition-colors duration-300 ${dark ? "bg-[#1C1714]" : "bg-[#F5F0EB]"}`}
    >
      <ThemeToggle />
      <Title />
      <div className="w-full max-w-3xl mt-4">
        <h2
          className={`mb-4 text-lg font-bold ${dark ? "text-[#A89880]" : "text-[#6B5744]"}`}
        >
          Your Feedback
        </h2>

        <div className="relative">
          <div
            ref={contentRef}
            className={`rounded-3xl border px-10 py-8 transition-colors duration-300 ${dark ? "bg-[#252019] border-[#2E2820]" : "bg-white border-[#E2D9CE]"}`}
          >
            <p
              className={`text-sm leading-relaxed whitespace-pre-wrap ${dark ? "text-[#C8B89A]" : "text-[#3D2E20]"}`}
            >
              {segments.map((seg, i) =>
                seg.annotationIndex !== null ? (
                  <mark
                    key={i}
                    ref={(el) => {
                      spanRefs.current[seg.annotationIndex!] = el;
                    }}
                    onClick={() =>
                      setActiveIndex(
                        activeIndex === seg.annotationIndex
                          ? null
                          : seg.annotationIndex,
                      )
                    }
                    className="cursor-pointer transition-colors"
                    style={{
                      background:
                        activeIndex === seg.annotationIndex
                          ? "#7f1d1d"
                          : "#fecaca",
                      color:
                        activeIndex === seg.annotationIndex
                          ? "#fecaca"
                          : "#991b1b",
                      borderRadius: "3px",
                      padding: "0 2px",
                    }}
                  >
                    {seg.text}
                  </mark>
                ) : (
                  <span key={i}>{seg.text}</span>
                ),
              )}
            </p>
          </div>

          {annotations.map((annotation, i) => (
            <div
              key={i}
              onClick={() => setActiveIndex(activeIndex === i ? null : i)}
              className="absolute cursor-pointer transition-all duration-200"
              style={{
                top: positions[i] ?? 0,
                left: "calc(100% + 16px)",
                width: "220px",
                zIndex: activeIndex === i ? 10 : 1,
              }}
            >
              <div
                className={`rounded-2xl border px-4 py-3 transition-all duration-200 ${
                  activeIndex === i
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
                <p
                  className={`text-xs leading-relaxed ${dark ? "text-[#A89880]" : "text-[#6B5744]"}`}
                >
                  {annotation.comment}
                </p>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={() =>
            navigate({ to: "/trained/$userId", params: { userId } })
          }
          className={`mt-4 px-6 py-2 rounded-full border text-sm font-bold transition-colors cursor-pointer ${
            dark
              ? "border-[#4A3E30] text-[#A89880] hover:bg-[#2E2820]"
              : "border-[#C8B89A] text-[#6B5744] hover:bg-[#EDE5DC]"
          }`}
        >
          ← Back
        </button>
      </div>
    </div>
  );
}
