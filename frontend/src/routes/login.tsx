import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { signIn, signUp } from "@/lib/auth";
import { Title } from "@/components/ui/Title";

export const Route = createFileRoute("/login")({
  component: LoginComponent,
});

function LoginComponent() {
  const navigate = useNavigate();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (isSignUp && password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    try {
      if (isSignUp) {
        await signUp(email, password);
      } else {
        await signIn(email, password);
      }
      navigate({ to: "/" });
    } catch (e) {
      setError(isSignUp ? "Could not create account" : "Invalid email or password");
    }
  };

  const handleToggle = () => {
    setIsSignUp((s) => !s);
    setError("");
    setConfirmPassword("");
  };

  return (
    <div className="min-h-screen bg-[#1C1714] flex flex-col items-center justify-center p-8">
      <Title />
      <div className="w-full max-w-sm bg-[#252019] rounded-3xl border border-[#2E2820] px-8 py-6 flex flex-col gap-4 mt-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full py-3 px-6 rounded-full border border-[#4A3E30] bg-[#3D3328] text-[#D4C4A8] placeholder:text-[#6B5C4A] focus:outline-none"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full py-3 px-6 rounded-full border border-[#4A3E30] bg-[#3D3328] text-[#D4C4A8] placeholder:text-[#6B5C4A] focus:outline-none"
        />
        {isSignUp && (
          <input
            type="password"
            placeholder="Confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={`w-full py-3 px-6 rounded-full border bg-[#3D3328] text-[#D4C4A8] placeholder:text-[#6B5C4A] focus:outline-none transition-colors ${
              confirmPassword && confirmPassword !== password
                ? "border-red-500"
                : "border-[#4A3E30]"
            }`}
          />
        )}
        {error && <p className="text-red-400 text-sm text-center">{error}</p>}
        <button
          onClick={handleSubmit}
          className="w-full py-3 rounded-full bg-red-500 text-white font-bold hover:bg-red-600 transition-colors cursor-pointer"
        >
          {isSignUp ? "Create account" : "Sign in"}
        </button>
        <p className="text-center text-sm text-[#6B5C4A]">
          {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={handleToggle}
            className="text-[#A89880] hover:text-[#D4C4A8] transition-colors cursor-pointer"
          >
            {isSignUp ? "Sign in" : "Sign up"}
          </button>
        </p>
      </div>
    </div>
  );
}