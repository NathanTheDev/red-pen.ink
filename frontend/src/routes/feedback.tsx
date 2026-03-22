import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Title } from "@/components/ui/Title";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { useTheme } from "@/context/ThemeContext";
import { zodValidator } from "@tanstack/zod-adapter";
import { z } from "zod";
import { useRef, useState, useEffect } from "react";
import { buildSegments } from "@/lib/feedback";
import { FeedbackCard } from "@/components/annotations/FeedbackCard";

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

        <FeedbackCard
          segments={segments}
          annotations={annotations}
          positions={positions}
          activeIndex={activeIndex}
          spanRefs={spanRefs}
          contentRef={contentRef}
          onMarkClick={(i) => setActiveIndex(activeIndex === i ? null : i)}
          dark={dark}
        />

        <button
          onClick={() =>
            navigate({ to: "/trained/$userId", params: { userId } })
          }
          className={`mt-4 px-6 py-2 rounded-full border text-sm font-bold transition-colors cursor-pointer ${dark ? "border-[#4A3E30] text-[#A89880] hover:bg-[#2E2820]" : "border-[#C8B89A] text-[#6B5744] hover:bg-[#EDE5DC]"}`}
        >
          ← Back
        </button>
      </div>
    </div>
  );
}
