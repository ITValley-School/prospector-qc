import { test, expect } from '@playwright/test';

test.describe('Prospector QC', () => {
	test('pagina principal carrega formulario', async ({ page }) => {
		await page.goto('/');
		await expect(page.locator('h1')).toHaveText('Nova Prospeccao');
		await expect(page.locator('input[placeholder*="Titulo"]')).toBeVisible();
		await expect(page.locator('input[placeholder*="Segmento"]')).toBeVisible();
	});

	test('navbar mostra todas as paginas', async ({ page }) => {
		await page.goto('/');
		await expect(page.locator('nav')).toContainText('Prospectar');
		await expect(page.locator('nav')).toContainText('Resultados');
		await expect(page.locator('nav')).toContainText('Historico');
		await expect(page.locator('nav')).toContainText('Configuracoes');
	});

	test('pagina resultados carrega', async ({ page }) => {
		await page.goto('/resultados');
		await expect(page.locator('h1')).toHaveText('Resultados');
	});

	test('pagina historico carrega com filtro', async ({ page }) => {
		await page.goto('/historico');
		await expect(page.locator('h1')).toHaveText('Historico');
		await expect(page.locator('input[placeholder*="Buscar"]')).toBeVisible();
	});

	test('pagina configuracoes carrega', async ({ page }) => {
		await page.goto('/configuracoes');
		await expect(page.locator('h1')).toHaveText('Configuracoes');
		await expect(page.locator('text=Claude Code CLI')).toBeVisible();
	});

	test('formulario valida campos obrigatorios', async ({ page }) => {
		await page.goto('/');
		await page.click('button:has-text("Prospectar")');
		await expect(page.locator('text=Preencha titulo e segmento')).toBeVisible();
	});

	test('navegacao entre paginas funciona', async ({ page }) => {
		await page.goto('/');
		await page.click('nav >> text=Resultados');
		await expect(page).toHaveURL('/resultados');
		await page.click('nav >> text=Historico');
		await expect(page).toHaveURL('/historico');
		await page.click('nav >> text=Configuracoes');
		await expect(page).toHaveURL('/configuracoes');
		await page.click('nav >> text=Prospectar');
		await expect(page).toHaveURL('/');
	});
});
