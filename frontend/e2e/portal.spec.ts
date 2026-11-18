import { expect, test, type Page } from "@playwright/test";

async function mockCandidateSession(page: Page) {
  await page.addInitScript(() => {
    localStorage.setItem("hireflow_access", "e2e-access");
    localStorage.setItem("hireflow_refresh", "e2e-refresh");
    localStorage.setItem("hireflow_user", JSON.stringify({ id: 7, email: "candidate@example.com", role: "CANDIDATE" }));
  });
  await page.route("**/api/v1/**", async (route) => {
    const url = route.request().url();
    if (url.endsWith("/candidates/profile/")) return route.fulfill({ json: { headline: "Product engineer", bio: "Builds useful things.", location: "Remote", years_experience: 4, portfolio_url: "" } });
    if (url.endsWith("/resumes/")) return route.fulfill({ json: [] });
    if (url.endsWith("/conversations/")) return route.fulfill({ json: [] });
    if (url.endsWith("/interviews/")) return route.fulfill({ json: [] });
    return route.fulfill({ json: {} });
  });
}

test.describe("portal workflows", () => {
  test("opens profile and resume toolkit", async ({ page }) => {
    await mockCandidateSession(page);
    await page.goto("/profile");
    await expect(page.getByRole("heading", { name: /make your story discoverable/i })).toBeVisible();
    await expect(page.getByRole("heading", { name: /profile details/i })).toBeVisible();
    await expect(page.getByText(/your latest signal/i)).toBeVisible();
  });

  test("opens resources and messages pages", async ({ page }) => {
    await mockCandidateSession(page);
    await page.goto("/resources");
    await expect(page.getByRole("heading", { name: /tools for your next move/i })).toBeVisible();
    await page.getByRole("link", { name: /open profile/i }).click();
    await expect(page).toHaveURL(/\/profile$/);
    await page.goto("/messages");
    await expect(page.getByRole("heading", { name: /keep the conversation moving/i })).toBeVisible();
    await expect(page.getByText(/select a conversation or start a new one/i)).toBeVisible();
  });

  test("opens candidate interview calendar", async ({ page }) => {
    await mockCandidateSession(page);
    await page.goto("/interviews");
    await expect(page.getByRole("heading", { name: /make time for the right conversations/i })).toBeVisible();
    await expect(page.getByText(/nothing scheduled yet/i)).toBeVisible();
  });

  test("completes local password reset flow", async ({ page }) => {
    await page.route("**/api/v1/auth/password-reset/", async (route) => route.fulfill({ json: { uid: "MQ", token: "valid-token" } }));
    await page.goto("/forgot-password");
    await page.getByLabel("Email address").fill("candidate@example.com");
    await page.getByRole("button", { name: /prepare reset link/i }).click();
    await expect(page).toHaveURL(/\/reset-password\?uid=MQ&token=valid-token/);
    await expect(page.getByRole("heading", { name: /choose a new password/i })).toBeVisible();
  });
});
