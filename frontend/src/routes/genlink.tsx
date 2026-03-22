import { createFileRoute, redirect } from "@tanstack/react-router";
import Session from "supertokens-web-js/recipe/session";
import { useState } from "react";

export const Route = createFileRoute("/genlink")({
  beforeLoad: async () => {
    const loggedIn = await Session.doesSessionExist();
    if (!loggedIn) throw redirect({ to: "/login" });
  },
  loader: async () => {
    return await Session.getUserId();
  },
  component: GenLinkComponent,
});

function GenLinkComponent() {
  const [copied, setCopied] = useState(false);
  const userId = Route.useLoaderData();
  const url = `http://localhost:3001/trained/${userId}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center justify-center p-8">
      <p className="text-[#A89880] text-sm font-bold mb-4">Trained link to provide to your students</p>
      <div className="flex items-center gap-3 w-full max-w-2xl bg-[#252019] border border-[#2E2820] rounded-full px-6 py-4">
        <span className="flex-1 text-red-400 font-mono text-lg truncate">{url}</span>
        <button
          onClick={handleCopy}
          className="shrink-0 px-5 py-2 rounded-full bg-red-500 text-white text-sm font-bold hover:bg-red-600 transition-colors cursor-pointer"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
    </div>
  );
}