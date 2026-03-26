<script lang="ts">
	interface Props {
		variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
		text: string;
	}

	let { variant = 'default', text }: Props = $props();

	const variantClasses: Record<string, string> = {
		default: 'bg-border/50 text-text-muted',
		success: 'bg-success/10 text-success border border-success/30',
		warning: 'bg-warning/10 text-warning border border-warning/30',
		danger: 'bg-danger/10 text-danger border border-danger/30',
		info: 'bg-accent/10 text-accent border border-accent/30',
	};
</script>

<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {variantClasses[variant]}">
	{text}
</span>
