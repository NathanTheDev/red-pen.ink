interface PButtonProps {
  content: string;
  submit: () => void;
  disabled?: boolean;
}

export function PButton({ content, submit, disabled = false }: PButtonProps) {
  return (
    <button
      onClick={submit}
      disabled={disabled}
      className="w-auto py-3 rounded-full bg-red-500 text-white font-bold hover:bg-red-600 transition-colors cursor-pointer"
    >
      {content}
    </button>
  );
}
