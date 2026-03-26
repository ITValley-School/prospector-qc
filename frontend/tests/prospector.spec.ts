import { test, expect } from '@playwright/test';

test.describe('Prospector QC', () => {
	test('pagina principal carrega formulario', async ({ page }) => {
		await page.goto('/');
		await expect(page.locator('h1')).toHaveText('Nova Prospeccao');
		await expect(page.locator('input[placeholder*="Empresas de tecnologia"]')).toBeVisible();
		await expect(page.locator('input[placeholder*="Tecnologia da Informacao"]')).toBeVisible();
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
		await expect(page.getByRole('heading', { name: 'Claude Code CLI' })).toBeVisible();
	});

	test('formulario valida campos obrigatorios', async ({ page }) => {
		await page.goto('/');
		await page.waitForLoadState('networkidle');
		await page.evaluate(() => {
			const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent?.includes('Prospectar'));
			btn?.click();
		});
		await expect(page.getByText('Preencha titulo e segmento')).toBeVisible();
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
