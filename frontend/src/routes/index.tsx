import * as React from "react";
import { useState } from "react";
import { createFileRoute, redirect, useNavigate } from "@tanstack/react-router";
import { Upload } from "@/components/ui/Upload";
import { Title } from "@/components/ui/Title";
import { Input } from "@/components/ui/Input";
import Session from "supertokens-web-js/recipe/session";

export const Route = createFileRoute("/")({
  beforeLoad: async () => {
    const loggedIn = await Session.doesSessionExist();
    if (!loggedIn) throw redirect({ to: "/login" });
  },
  component: HomeComponent,
});

function HomeComponent() {
  const navigate = useNavigate();
  const [goodFiles, setGoodFiles] = useState<File[]>([]);
  const [markedFiles, setMarkedFiles] = useState<File[]>([]);
  const [moduleContext, setModuleContext] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (goodFiles.length === 0 || markedFiles.length === 0 || !moduleContext) {
      setError("Please fill in all fields before submitting.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      goodFiles.forEach((f) => formData.append("good", f));
      markedFiles.forEach((f) => formData.append("marked", f));
      formData.append("module_context", moduleContext);

      const response = await fetch("http://localhost:8080/ingest", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      navigate({ to: "/genlink" });

    } catch (e) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center p-8">
      <Title />
      <div className="w-full max-w-xl bg-[#252019] rounded-3xl shadow-sm border border-[#2E2820] px-8 py-6 mt-4">
        <Upload
          label="Upload an example of an essay you would give 100%"
          content="Upload a .docx file..."
          files={goodFiles}
          onFilesChange={setGoodFiles}
        />
        <Upload
          label="Upload some examples of essays you have provided feedback on"
          content="Upload several .docx files..."
          multiple={true}
          files={markedFiles}
          onFilesChange={setMarkedFiles}
        />
        <Input
          label="Please provide some context as to the HSC module these files relate to"
          placeholder="These responses are for Module C Discursive..."
          value={moduleContext}
          onChange={(e) => setModuleContext(e.target.value)}
        />
        {error && <p className="text-red-400 text-sm text-center mt-4">{error}</p>}
        <div className="flex justify-center mt-6">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-8 py-3 rounded-full bg-red-500 text-white font-bold hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Uploading..." : "Submit"}
          </button>
        </div>
      </div>
    </div>
  );
}