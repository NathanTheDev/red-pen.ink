import * as React from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Upload } from "@/components/teacher/upload/Upload";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  return (
    <div className="p-2">
      <Upload />
    </div>
  );
}
