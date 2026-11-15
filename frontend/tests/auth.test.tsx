import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import LoginPage from "../src/features/auth/LoginPage";
import RegisterPage from "../src/features/auth/RegisterPage";

describe("authentication screens", () => {
  it("renders the login form", () => {
    render(<MemoryRouter><LoginPage /></MemoryRouter>);
    expect(screen.getByRole("heading", { name: /sign in to your next chapter/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it("renders candidate registration fields", () => {
    render(<MemoryRouter><RegisterPage /></MemoryRouter>);
    expect(screen.getByRole("heading", { name: /create your next chapter/i })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "Candidate" })).toBeInTheDocument();
  });

  it("requires registration fields", async () => {
    const user = userEvent.setup();
    render(<MemoryRouter><RegisterPage /></MemoryRouter>);
    await user.click(screen.getByRole("button", { name: /create account/i }));
    expect(screen.getByLabelText(/email/i)).toBeInvalid();
  });
});
