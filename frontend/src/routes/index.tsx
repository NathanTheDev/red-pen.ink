import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Upload } from "@/components/ui/Upload";
import { Title } from "@/components/ui/Title";
import { Input } from "@/components/ui/Input";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  return (
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center p-8">
      <Title />
      <div className="w-full max-w-xl bg-[#252019] rounded-3xl shadow-sm border border-[#2E2820] px-8 py-6 mt-4">
        <Upload
          label="Upload an example of an essay you would give 100%"
          content="Upload a .docx file..."
        />
        <Upload
          label="Upload some examples of essays you have provided feedback on"
          content="Upload several .docx files..."
          multiple={true}
        />
        <Input
          label="Please provide some context as to the HSC module these files relate to"
          placeholder="These responses are for Module C Discursive..."
        />
      </div>
    </div>
  );
}