import { expect, test } from "@playwright/test";

test.describe("authentication flow", () => {
  test("renders login and validates required fields", async ({ page }) => {
    await page.goto("/login");
    await expect(page.getByRole("heading", { name: /sign in to your next chapter/i })).toBeVisible();
    await expect(page.getByLabel("Email address")).toBeVisible();
    await expect(page.getByLabel("Password")).toBeVisible();
    await page.getByRole("button", { name: /sign in/i }).click();
    const email = page.getByLabel("Email address");
    await expect.poll(async () => email.evaluate((element) => (element as HTMLInputElement).validity.valid)).toBe(false);
  });

  test("navigates from login to registration", async ({ page }) => {
    await page.goto("/login");
    await page.getByRole("link", { name: /create an account/i }).click();
    await expect(page).toHaveURL(/\/register$/);
    await expect(page.getByRole("heading", { name: /create your next chapter/i })).toBeVisible();
    await expect(page.locator("select option")).toHaveText(["Candidate", "Recruiter"]);
  });
});
