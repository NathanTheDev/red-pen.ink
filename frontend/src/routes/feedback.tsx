import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Title } from "@/components/ui/Title";
import { zodValidator } from "@tanstack/zod-adapter";
import { z } from "zod";

const feedbackSearchSchema = z.object({
  userId: z.string(),
  annotations: z.array(z.object({
    span: z.string(),
    comment: z.string(),
  })),
});

export const Route = createFileRoute("/feedback")({
  validateSearch: zodValidator(feedbackSearchSchema),
  component: FeedbackComponent,
});

function FeedbackComponent() {
  const navigate = useNavigate();
  const { annotations, userId } = Route.useSearch();

  return (
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center p-8">
      <Title />
      <div className="w-full max-w-xl bg-[#252019] rounded-3xl shadow-sm border border-[#2E2820] px-8 py-6 mt-4">
        <h2 className="text-lg font-bold text-[#A89880] mb-6">Your Feedback</h2>
        <div className="flex flex-col gap-4">
          {annotations.map((annotation, i) => (
            <div
              key={i}
              className="rounded-2xl border border-[#2E2820] bg-[#1C1714] px-6 py-4"
            >
              <p className="text-red-400 font-mono text-sm mb-2">"{annotation.span}"</p>
              <p className="text-[#A89880] text-sm">{annotation.comment}</p>
            </div>
          ))}
        </div>
        <div className="flex justify-center mt-8">
          <button
            onClick={() => navigate({ to: "/trained/$userId", params: { userId } })}
            className="px-8 py-3 rounded-full border border-[#4A3E30] text-[#A89880] text-sm font-bold hover:bg-[#2E2820] transition-colors"
          >
            ← Back
          </button>
        </div>
      </div>
    </div>
  );
}