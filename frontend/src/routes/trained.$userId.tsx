import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Upload } from "@/components/ui/Upload";
import { Title } from "@/components/ui/Title";

export const Route = createFileRoute("/trained/$userId")({
  component: TrainedComponent,
});

function TrainedComponent() {
  const { userId } = Route.useParams();
  const navigate = useNavigate();
  const [file, setFile] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (file.length === 0) {
      setError("Please upload an essay before submitting.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file[0]);

      const response = await fetch("http://localhost:8080/check", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const annotations = await response.json();

      navigate({
        to: "/feedback",
        search: {
          annotations,
          userId,
        },
      });
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
          label="Upload your essay for feedback"
          content="Upload a .docx file..."
          files={file}
          onFilesChange={setFile}
        />
        {error && (
          <p className="text-red-400 text-sm text-center mt-4">{error}</p>
        )}
        <div className="flex justify-center mt-6">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-8 py-3 rounded-full bg-red-500 text-white font-bold hover:bg-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Uploading..." : "Get Feedback"}
          </button>
        </div>
      </div>
    </div>
  );
}
