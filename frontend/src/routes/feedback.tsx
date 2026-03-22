import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Title } from "@/components/ui/Title";
import { zodValidator } from "@tanstack/zod-adapter";
import { z } from "zod";
import { useRef, useState, useEffect } from "react";

const feedbackSearchSchema = z.object({
  userId: z.string(),
  annotations: z.array(
    z.object({
      span: z.string(),
      comment: z.string(),
    }),
  ),
  content: z.string(),
});

export const Route = createFileRoute("/feedback")({
  validateSearch: zodValidator(feedbackSearchSchema),
  component: FeedbackComponent,
});

type AnnotationWithPosition = {
  span: string;
  comment: string;
  top: number;
};

function buildSegments(
  content: string,
  annotations: { span: string; comment: string }[],
) {
  type Match = { start: number; end: number; index: number };
  const matches: Match[] = [];

  for (let i = 0; i < annotations.length; i++) {
    const idx = content.indexOf(annotations[i].span);
    if (idx !== -1) {
      matches.push({
        start: idx,
        end: idx + annotations[i].span.length,
        index: i,
      });
    }
  }

  matches.sort((a, b) => a.start - b.start);

  const segments: { text: string; annotationIndex: number | null }[] = [];
  let cursor = 0;

  for (const match of matches) {
    if (match.start > cursor) {
      segments.push({
        text: content.slice(cursor, match.start),
        annotationIndex: null,
      });
    }
    segments.push({
      text: content.slice(match.start, match.end),
      annotationIndex: match.index,
    });
    cursor = match.end;
  }

  if (cursor < content.length) {
    segments.push({ text: content.slice(cursor), annotationIndex: null });
  }

  return segments;
}

function FeedbackComponent() {
  const navigate = useNavigate();
  const { annotations, userId, content } = Route.useSearch();
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
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center p-8">
      <Title />
      <div className="w-full max-w-5xl mt-4">
        <h2 className="mb-4 text-lg font-bold text-[#A89880]">Your Feedback</h2>

        {/* Relative container so comments can be positioned against it */}
        <div className="relative">
          {/* Content at normal page width */}
          <div
            ref={contentRef}
            className="bg-[#252019] rounded-3xl border border-[#2E2820] px-10 py-8"
          >
            <p className="text-[#C8B89A] text-sm leading-relaxed whitespace-pre-wrap">
              {segments.map((seg, i) =>
                seg.annotationIndex !== null ? (
                  <mark
                    key={i}
                    ref={(el) => { spanRefs.current[seg.annotationIndex!] = el; }}
                    onClick={() =>
                      setActiveIndex(activeIndex === seg.annotationIndex ? null : seg.annotationIndex)
                    }
                    className="cursor-pointer rounded px-0.5 transition-colors"
                    style={{
                      background: "transparent",
                      color: activeIndex === seg.annotationIndex ? "#f87171" : "#ef4444",
                      textDecoration: "underline",
                      textDecorationColor: activeIndex === seg.annotationIndex ? "#f87171" : "#991b1b",
                      textUnderlineOffset: "3px",
                    }}
                  >
                    {seg.text}
                  </mark>
                ) : (
                  <span key={i}>{seg.text}</span>
                )
              )}
            </p>
          </div>

          {/* Comments anchored to right margin, outside content box */}
          {annotations.map((annotation, i) => (
            <div
              key={i}
              onClick={() => setActiveIndex(activeIndex === i ? null : i)}
              className="absolute cursor-pointer transition-all duration-200"
              style={{
                top: positions[i] ?? 0,
                left: "calc(100% + 16px)",
                width: "220px",
              }}
            >
              <div
                className={`rounded-2xl border px-4 py-3 transition-all duration-200 ${
                  activeIndex === i
                    ? "border-red-500/50 bg-[#2E1A1A] shadow-lg shadow-red-900/20"
                    : "border-[#2E2820] bg-[#252019] opacity-60 hover:opacity-100"
                }`}
              >
                <p className="text-red-400 font-mono text-xs mb-1 truncate">
                  "{annotation.span}"
                </p>
                <p className="text-[#A89880] text-xs leading-relaxed">
                  {annotation.comment}
                </p>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={() => navigate({ to: "/trained/$userId", params: { userId } })}
          className="mt-4 px-6 py-2 rounded-full border border-[#4A3E30] text-[#A89880] text-sm font-bold hover:bg-[#2E2820] transition-colors cursor-pointer"
        >
          ← Back
        </button>
      </div>
    </div>
  );
}