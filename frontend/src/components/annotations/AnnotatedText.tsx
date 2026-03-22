import { Segment } from "@/types";
import { RefObject } from "react";

type AnnotatedTextProps = {
  segments: Segment[];
  activeIndex: number | null;
  spanRefs: RefObject<(HTMLElement | null)[]>;
  onMarkClick: (index: number) => void;
  dark: boolean;
};

export function AnnotatedText({
  segments,
  activeIndex,
  spanRefs,
  onMarkClick,
  dark,
}: AnnotatedTextProps) {
  return (
    <p className={`text-sm leading-relaxed whitespace-pre-wrap ${dark ? "text-[#C8B89A]" : "text-[#3D2E20]"}`}>
      {segments.map((seg, i) =>
        seg.annotationIndex !== null ? (
          <mark
            key={i}
            ref={(el) => { spanRefs.current[seg.annotationIndex!] = el; }}
            onClick={() => onMarkClick(seg.annotationIndex!)}
            className="cursor-pointer transition-colors"
            style={{
              background: activeIndex === seg.annotationIndex ? "#7f1d1d" : "#fecaca",
              color: activeIndex === seg.annotationIndex ? "#fecaca" : "#991b1b",
              borderRadius: "3px",
              padding: "0 2px",
            }}
          >
            {seg.text}
          </mark>
        ) : (
          <span key={i}>{seg.text}</span>
        )
      )}
    </p>
  );
}