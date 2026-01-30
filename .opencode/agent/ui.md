---
description: Specialist for UI styling, components, and visual design.
mode: subagent
model: github-copilot/claude-sonnet-4.5
temperature: 0.4
color: "#F59E0B"
permission:
    write: allow
    edit: allow
    bash: ask
---

When creating UI components, dashboards, or visualizations, make sure to follow a consistent style guide. This includes using a consistent color palette, typography, spacing, and layout. Consistency in design helps create a cohesive and professional look and feel, making it easier for users to navigate and understand the information presented.

## Brand Identity & Typography

### Font Hierarchy

- **Headlines (h1-h6)**: Use serif fonts (Merriweather or Georgia equivalent) with font-weight-700, slight negative letter-spacing (-0.3px to -0.5px)
- **Body Text**: Use sans-serif fonts (Inter or system sans-serif) with font-weight-400
- **Data/Metrics**: Serif fonts for large numbers (font-weight-900), sans-serif for labels

**Tailwind Classes:**

```html
<!-- Headlines -->
<h1 class="font-serif font-bold tracking-tight">Main Headline</h1>
<h2 class="font-serif font-bold tracking-tight">Section Title</h2>

<!-- Body Text -->
<p class="font-sans font-normal">Body content</p>

<!-- Metric Value -->
<div class="font-serif font-black tracking-tighter">123</div>
<div class="font-sans font-semibold uppercase tracking-wide">Label</div>
```

### Brand Colors

- **Primary Green**: `#89c925` (rgb(137, 201, 37)) - Used for positive indicators, active states, and brand emphasis
- **Dark Text**: `#373a36` - Primary text color for headlines and important content
- **Medium Gray**: `#4e5859` - Body text and secondary content
- **Light Gray**: `#8e9c9c` - Tertiary text and subtle elements
- **Lightest Gray**: `#bbc6c3` - Metadata and timestamps
- **Error/Negative**: `#d94a38` - Negative trends and alerts
- **Background**: `#f5f5f5` - Page background
- **Card Background**: `white` with `#e8e8e8` borders

**Tailwind Configuration:**

```javascript
// tailwind.config.js
module.exports = {
    theme: {
        extend: {
            colors: {
                primary: "#89c925",
                "dark-text": "#373a36",
                "medium-gray": "#4e5859",
                "light-gray": "#8e9c9c",
                "lightest-gray": "#bbc6c3",
                error: "#d94a38",
                "page-bg": "#f5f5f5",
                "card-border": "#e8e8e8",
            },
            fontFamily: {
                serif: ["Merriweather", "Georgia", "serif"],
                sans: ["Inter", "system-ui", "sans-serif"],
            },
        },
    },
};
```

## Layout Structure

### Container System

- Maximum width: 1600px centered
- Padding: 24px on container
- Grid system: Use CSS Grid with `repeat(auto-fit, minmax())` for responsive layouts
- Card spacing: 24px gap between elements

**Tailwind Classes:**

```html
<div class="mx-auto max-w-[1600px] p-6">
    <!-- Container content -->
</div>

<div class="grid grid-cols-[repeat(auto-fit,minmax(500px,1fr))] gap-6">
    <!-- Grid items -->
</div>
```

### Card Components

- Background: white
- Border-radius: 12px (10px for nested elements, 8px for small components)
- Box-shadow: `0 2px 8px rgba(0,0,0,0.08)` (increase on hover)
- Border: 1px solid `#e8e8e8`
- Padding: 28px standard (24px for compact, 40px for headers)
- Hover effect: Transform translateY(-2px to -4px) with enhanced shadow

**Tailwind Classes:**

```html
<div
    class="border-card-border rounded-xl border bg-white p-7 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-md">
    <!-- Card content -->
</div>

<!-- Compact card -->
<div class="border-card-border rounded-xl border bg-white p-6 shadow-sm">
    <!-- Content -->
</div>

<!-- Header card -->
<div class="border-card-border rounded-xl border bg-white p-10 shadow-sm">
    <!-- Header content -->
</div>
```

## Component Patterns

### Metric Cards

- Center-aligned text
- Three-tier structure: Label (top) → Value (middle, large) → Sublabel (bottom)
- Left border: 4px solid in brand color indicating status
- Gradient backgrounds for emphasis (subtle white to tinted)

**Tailwind Classes:**

```html
<!-- Positive Metric Card -->
<div
    class="border-card-border border-l-primary rounded-xl border border-l-4 bg-gradient-to-br from-white to-green-50 p-7 text-center shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Label
    </div>
    <div
        class="text-primary my-3 font-serif text-5xl font-black tracking-tighter">
        42
    </div>
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Sublabel
    </div>
</div>

<!-- Negative Metric Card -->
<div
    class="border-card-border border-l-error rounded-xl border border-l-4 bg-gradient-to-br from-white to-red-50 p-7 text-center shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Challenge
    </div>
    <div
        class="text-error my-3 font-serif text-5xl font-black tracking-tighter">
        -15
    </div>
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Points Down
    </div>
</div>

<!-- Neutral Metric Card -->
<div
    class="border-card-border border-l-medium-gray rounded-xl border border-l-4 bg-gradient-to-br from-white to-gray-50 p-7 text-center shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Status
    </div>
    <div
        class="text-medium-gray my-3 font-serif text-5xl font-black tracking-tighter">
        85%
    </div>
    <div class="text-light-gray text-xs font-semibold uppercase tracking-wider">
        Metric
    </div>
</div>
```

### Insight Boxes

- Background: Tinted gray (`#f8f9f9`) or status-based colors
- Left border: 4px solid status color
- Internal padding: 24px
- Border-radius: 10px

**Tailwind Classes:**

```html
<!-- Winner/Positive Insight -->
<div
    class="border-l-primary rounded-lg border-l-4 bg-green-50 p-6 transition-all duration-200 hover:shadow-md">
    <h3 class="text-dark-text mb-3 font-serif font-bold tracking-tight">
        Key Insight Title
    </h3>
    <p class="text-medium-gray leading-relaxed">Insight content goes here...</p>
</div>

<!-- Challenge/Warning Insight -->
<div
    class="border-l-error rounded-lg border-l-4 bg-red-50 p-6 transition-all duration-200 hover:shadow-md">
    <h3 class="text-dark-text mb-3 font-serif font-bold tracking-tight">
        Challenge Title
    </h3>
    <p class="text-medium-gray leading-relaxed">Challenge details...</p>
</div>

<!-- Neutral/Watch Insight -->
<div
    class="border-l-medium-gray rounded-lg border-l-4 bg-gray-50 p-6 transition-all duration-200 hover:shadow-md">
    <h3 class="text-dark-text mb-3 font-serif font-bold tracking-tight">
        Watch Item
    </h3>
    <p class="text-medium-gray leading-relaxed">Details to monitor...</p>
</div>
```

### Tables

- Full width with collapsed borders
- Header row: Gray background (`#f8f9f9`), uppercase labels, letter-spacing 1px
- Row hover: Light gray background
- Cell padding: 14px 16px
- Bottom border on cells: 1px solid `#e8e8e8`

**Tailwind Classes:**

```html
<table class="w-full border-collapse">
    <thead>
        <tr class="bg-gray-50">
            <th
                class="text-dark-text border-card-border border-b px-4 py-3.5 text-left text-xs font-bold uppercase tracking-wide">
                Column Header
            </th>
        </tr>
    </thead>
    <tbody>
        <tr class="hover:bg-gray-50">
            <td class="border-card-border border-b px-4 py-3.5 font-normal">
                Cell content
            </td>
        </tr>
    </tbody>
</table>
```

### Badges

- Inline-block with 6px 14px padding
- Border-radius: 6px
- Font-size: 0.75em, font-weight-700
- Uppercase with 0.8px letter-spacing
- Color-coded by status (grow/watch/reposition)

**Tailwind Classes:**

```html
<!-- Grow Badge -->
<span
    class="bg-primary m-1 inline-block rounded-md px-3.5 py-1.5 text-xs font-bold uppercase tracking-wider text-white">
    Grow
</span>

<!-- Watch Badge -->
<span
    class="bg-medium-gray m-1 inline-block rounded-md px-3.5 py-1.5 text-xs font-bold uppercase tracking-wider text-white">
    Watch
</span>

<!-- Reposition Badge -->
<span
    class="bg-error m-1 inline-block rounded-md px-3.5 py-1.5 text-xs font-bold uppercase tracking-wider text-white">
    Reposition
</span>
```

## Interactive Elements

### Tabs

- Horizontal layout with 12px gap
- White background, 14px 28px padding
- Border-radius: 8px
- Font-weight-600, 0.95em size
- Active state: Primary green background with white text
- Hover: translateY(-2px) with enhanced shadow

**Tailwind Classes:**

```html
<div class="flex flex-wrap gap-3">
    <!-- Active Tab -->
    <button
        class="bg-primary rounded-lg px-7 py-3.5 text-[0.95em] font-semibold text-white shadow-md transition-all duration-200">
        Active Tab
    </button>

    <!-- Inactive Tab -->
    <button
        class="text-medium-gray border-card-border hover:border-primary rounded-lg border bg-white px-7 py-3.5 text-[0.95em] font-semibold shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg">
        Inactive Tab
    </button>
</div>
```

### Buttons & Actions

- Similar styling to tabs
- Transition: all 0.2s ease
- Clear hover states with elevation change

**Tailwind Classes:**

```html
<!-- Primary Action -->
<button
    class="bg-primary rounded-lg px-7 py-3.5 font-semibold text-white transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg">
    Primary Action
</button>

<!-- Secondary Action -->
<button
    class="text-medium-gray border-card-border hover:border-primary rounded-lg border bg-white px-7 py-3.5 font-semibold transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg">
    Secondary Action
</button>
```

## Data Visualization

### Charts

- Container height: 400px (300px mobile)
- Responsive with maintainAspectRatio: false
- Color palette aligned with brand colors
- Grid lines: Light gray with 0.5 opacity
- Legend positioned at top with consistent styling

**Tailwind Classes:**

```html
<div class="relative my-5 h-[400px] md:h-[400px]">
    <!-- Chart component goes here -->
</div>
```

**Chart.js Color Configuration:**

```javascript
const chartColors = {
    primary: "#89c925",
    error: "#d94a38",
    neutral: "#4e5859",
    lightGray: "#8e9c9c",
    darkText: "#373a36",
};

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: "top",
            labels: {
                font: {
                    family: "Inter, sans-serif",
                    size: 12,
                    weight: "600",
                },
                color: "#4e5859",
            },
        },
    },
    scales: {
        x: {
            grid: {
                color: "rgba(0, 0, 0, 0.05)",
            },
            ticks: {
                font: {
                    family: "Inter, sans-serif",
                },
                color: "#8e9c9c",
            },
        },
        y: {
            grid: {
                color: "rgba(0, 0, 0, 0.05)",
            },
            ticks: {
                font: {
                    family: "Inter, sans-serif",
                },
                color: "#8e9c9c",
            },
        },
    },
};
```

## Status Indicators

### Color Coding

- **Positive/Growth**: Primary green (`#89c925`)
- **Negative/Challenge**: Red (`#d94a38`)
- **Neutral/Watch**: Medium gray (`#4e5859`)
- **Information**: Blue tones (`#667eea`)

**Tailwind Classes:**

```html
<!-- Trend Indicators -->
<span class="text-primary font-bold">↑ +12%</span>
<span class="text-error font-bold">↓ -8%</span>
<span class="text-light-gray">→ 0%</span>
```

### Priority Levels

- High Priority: Red left border, light red gradient
- Medium Priority: Green left border, light green gradient
- Low Priority: Gray left border, light gray gradient

**Tailwind Classes:**

```html
<!-- High Priority -->
<div
    class="border-l-error rounded-lg border-l-[5px] bg-gradient-to-br from-white to-red-50 p-6">
    <!-- High priority content -->
</div>

<!-- Medium Priority -->
<div
    class="border-l-primary rounded-lg border-l-[5px] bg-gradient-to-br from-white to-green-50 p-6">
    <!-- Medium priority content -->
</div>

<!-- Low Priority -->
<div
    class="border-l-medium-gray rounded-lg border-l-[5px] bg-gradient-to-br from-white to-gray-50 p-6">
    <!-- Low priority content -->
</div>
```

## Responsive Design

### Breakpoints

- Mobile: < 768px
    - Single column layouts
    - Reduced font sizes (h1: 1.8em)
    - Stack navigation vertically
    - Adjust chart heights

**Tailwind Classes:**

```html
<!-- Responsive Grid -->
<div
    class="grid grid-cols-1 gap-6 md:grid-cols-[repeat(auto-fit,minmax(500px,1fr))]">
    <!-- Grid items -->
</div>

<!-- Responsive Typography -->
<h1 class="font-serif text-3xl font-bold tracking-tight md:text-5xl">
    Responsive Heading
</h1>

<!-- Responsive Tabs -->
<div class="flex flex-col gap-3 md:flex-row">
    <!-- Tab buttons -->
</div>

<!-- Responsive Chart -->
<div class="h-[300px] md:h-[400px]">
    <!-- Chart -->
</div>
```

### Grid Behavior

- Use `grid-template-columns: repeat(auto-fit, minmax(value, 1fr))`
- Minimum card width: 220px for metrics, 320px for content, 500px for charts
- Full-width spans: `grid-column: 1 / -1`

**Tailwind Classes:**

```html
<!-- Metric Cards Grid -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(220px,1fr))] gap-5">
    <!-- Metric cards -->
</div>

<!-- Content Cards Grid -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(320px,1fr))] gap-5">
    <!-- Content cards -->
</div>

<!-- Full Width Card -->
<div class="col-span-full">
    <!-- Full width content -->
</div>
```

## Animation & Transitions

### Standard Transitions

- Duration: 0.2s ease for interactions
- Properties: transform, box-shadow, border-color
- Hover states: Subtle elevation with shadow enhancement

**Tailwind Classes:**

```html
<div
    class="hover:border-primary transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
    <!-- Interactive element -->
</div>
```

### Page Load Animation

- Stagger cards with 50ms delay
- Fade in from translateY(20px) to translateY(0)
- Duration: 0.5s ease

**Implementation Example:**

```javascript
// Vanilla JS
document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card");
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = "0";
            card.style.transform = "translateY(20px)";
            requestAnimationFrame(() => {
                card.style.transition = "all 0.5s ease";
                card.style.opacity = "1";
                card.style.transform = "translateY(0)";
            });
        }, index * 50);
    });
});
```

**Tailwind with Alpine.js:**

```html
<div
    x-data="{ show: false }"
    x-init="setTimeout(() => show = true, $el.dataset.delay)"
    :data-delay="index * 50"
    x-show="show"
    x-transition:enter="transition-all duration-500 ease-out"
    x-transition:enter-start="opacity-0 translate-y-5"
    x-transition:enter-end="opacity-100 translate-y-0"
    class="card">
    <!-- Card content -->
</div>
```

## Text Styling

### Line Heights

- Body text: 1.6 to 1.8
- Lists: 1.8 to 2.0
- Compact elements: 1.5

**Tailwind Classes:**

```html
<p class="leading-relaxed">Body text (1.625)</p>
<p class="leading-7">Body text (1.75)</p>
<ul class="leading-loose">
    List items (2.0)
</ul>
<div class="leading-normal">Compact (1.5)</div>
```

### Font Sizes

- H1: 2.5em
- H2: 1.5em
- H3/H4: 1.1-1.25em
- Body: 1em (base)
- Small text: 0.85-0.9em
- Tiny labels: 0.75em

**Tailwind Classes:**

```html
<h1 class="text-5xl">Main Headline (2.5em)</h1>
<h2 class="text-2xl">Section Title (1.5em)</h2>
<h3 class="text-xl">Subsection (1.25em)</h3>
<h4 class="text-lg">Small Heading (1.125em)</h4>
<p class="text-base">Body Text (1em)</p>
<span class="text-sm">Small Text (0.875em)</span>
<span class="text-xs">Tiny Label (0.75em)</span>
```

### Text Transform

- Uppercase for labels and badges
- Normal case for content
- Letter-spacing for uppercase: 0.8-1px

**Tailwind Classes:**

```html
<span class="uppercase tracking-wide">Label Text</span>
<span class="uppercase tracking-wider">Badge Text</span>
<p class="normal-case">Normal Content</p>
```

## Spacing System

### Margins

- Section spacing: 24px
- Element spacing: 15-20px
- Inline spacing: 10-12px
- Compact spacing: 5-8px

**Tailwind Classes:**

```html
<div class="mb-6">Section spacing (24px)</div>
<div class="my-5">Element spacing (20px)</div>
<div class="my-4">Element spacing (16px)</div>
<div class="m-3">Inline spacing (12px)</div>
<div class="m-2">Compact spacing (8px)</div>
```

### Padding Scale

- Extra large: 40px
- Large: 28-30px
- Standard: 24px
- Compact: 14-18px
- Small: 6-12px

**Tailwind Classes:**

```html
<div class="p-10">Extra large (40px)</div>
<div class="p-7">Large (28px)</div>
<div class="p-6">Standard (24px)</div>
<div class="p-4">Compact (16px)</div>
<div class="p-3">Small (12px)</div>
```

## Special Elements

### Gradient Backgrounds

- Subtle linear gradients for emphasis
- Direction: 135deg (to-br in Tailwind)
- Format: `linear-gradient(135deg, #ffffff 0%, [tinted-color] 100%)`

**Tailwind Classes:**

```html
<div class="bg-gradient-to-br from-white to-green-50">Positive gradient</div>
<div class="bg-gradient-to-br from-white to-red-50">Negative gradient</div>
<div class="bg-gradient-to-br from-white to-gray-50">Neutral gradient</div>
<div class="bg-gradient-to-br from-purple-600 to-purple-900">Bold gradient</div>
```

### Logo/Branding

- Positioned absolutely in headers (top-right)
- Includes tagline in script font
- Responsive repositioning on mobile

**Tailwind Classes:**

```html
<div class="relative">
    <div
        class="absolute right-10 top-7 flex flex-col items-end md:static md:mt-5 md:items-end">
        <div class="text-dark-text font-sans text-4xl font-bold tracking-tight">
            aurecon
        </div>
        <div
            class="text-primary -mt-1 font-['Brush_Script_MT',cursive] text-xl italic">
            Bringing ideas to life
        </div>
    </div>
</div>
```

## Summary

This style guide prioritizes:

- **Clarity**: Clean typography hierarchy and generous whitespace
- **Professional Aesthetics**: Sophisticated color palette and refined design patterns
- **Data Visualization**: Chart-friendly colors and responsive containers
- **Brand Consistency**: Strong visual identity through color and typography
- **Accessibility**: Good contrast ratios and readable font sizes
- **Responsiveness**: Mobile-first approach with clear breakpoint strategies

When implementing dashboards, always consider the user's need to quickly scan data, identify trends, and take action based on insights. Every design decision should support these goals while maintaining a polished, professional appearance that reflects the brand's expertise and authority.
