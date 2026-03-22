import { useRef, RefObject } from "react";
import { AnnotatedText } from "./AnnotatedText";
import { AnnotationCard } from "./AnnotationCard";
import { Segment } from "@/types";

type FeedbackCardProps = {
  segments: Segment[];
  annotations: { span: string; comment: string }[];
  positions: number[];
  activeIndex: number | null;
  spanRefs: RefObject<(HTMLElement | null)[]>;
  contentRef: RefObject<HTMLDivElement | null>;
  onMarkClick: (index: number) => void;
  dark: boolean;
};

export function FeedbackCard({
  segments,
  annotations,
  positions,
  activeIndex,
  spanRefs,
  contentRef,
  onMarkClick,
  dark,
}: FeedbackCardProps) {
  return (
    <div className="relative">
      <div
        ref={contentRef}
        className={`rounded-3xl border px-10 py-8 transition-colors duration-300 ${dark ? "bg-[#252019] border-[#2E2820]" : "bg-white border-[#E2D9CE]"}`}
      >
        <AnnotatedText
          segments={segments}
          activeIndex={activeIndex}
          spanRefs={spanRefs}
          onMarkClick={onMarkClick}
          dark={dark}
        />
      </div>

      {annotations.map((annotation, i) => (
        <AnnotationCard
          key={i}
          annotation={annotation}
          index={i}
          isActive={activeIndex === i}
          position={positions[i]}
          onClick={() => onMarkClick(i)}
          dark={dark}
        />
      ))}
    </div>
  );
}