export function buildSegments(
  content: string,
  annotations: { span: string; comment: string }[],
) {
  type Match = { start: number; end: number; index: number };
  const matches: Match[] = [];

  for (let i = 0; i < annotations.length; i++) {
    const idx = content.indexOf(annotations[i].span);
    if (idx !== -1)
      matches.push({
        start: idx,
        end: idx + annotations[i].span.length,
        index: i,
      });
  }

  matches.sort((a, b) => a.start - b.start);

  const segments: { text: string; annotationIndex: number | null }[] = [];
  let cursor = 0;

  for (const match of matches) {
    if (match.start > cursor)
      segments.push({
        text: content.slice(cursor, match.start),
        annotationIndex: null,
      });
    segments.push({
      text: content.slice(match.start, match.end),
      annotationIndex: match.index,
    });
    cursor = match.end;
  }

  if (cursor < content.length)
    segments.push({ text: content.slice(cursor), annotationIndex: null });

  return segments;
}