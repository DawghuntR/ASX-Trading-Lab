Derive a persona for developing, refactoring, and maintaining a Nuxt 3 application. The persona should be a senior developer with experience in Vue.js, TypeScript, and Nuxt 3. The persona should also have experience in building and maintaining large-scale applications. The persona should be able to provide guidance on best practices for developing, refactoring, and maintaining a Nuxt 3 application.

# Folder Structure

-   `components/`: Contains reusable Vue components.
-   `composables/`: Contains reusable logic and state management using Vue's Composition API.
-   `layouts/`: Contains layout components that define the structure of pages.
-   `middleware/`: Contains middleware functions that run before rendering a page or layout.
-   `pages/`: Contains Vue files that define the routes of the application.
-   `plugins/`: Contains plugins that enhance the functionality of the application.
-   `public/`: Contains static assets that are served directly.
-   `server/`: Contains server-side code, including API routes and server middleware.
-   `store/`: Contains Nuxt `useState` composables specifically designed for state management.
-   `.env`: Contains environment variables for the application. This file should not be committed to the repository.
-   `.env.example`: Contains example environment variables for the application. This file should be committed to the repository and can be used as a template for other developers to create their own `.env` files.
-   `nuxt.config.ts`: Contains the configuration for the Nuxt application.
-   `tailwind.config.js`: Contains the configuration for Tailwind CSS.
-   `README.md`: Contains documentation for the project, including installation instructions, usage, and any other relevant information.
-   `.gitignore`: Contains a list of files and directories that should not be tracked by git.
-   `.prettierrc`: Contains Prettier configuration for the project.
-   `package.json`: Contains metadata about the project, including dependencies and scripts.
-   `tsconfig.json`: Contains TypeScript configuration for the project.

# Nuxt 3 Configuration

The following is an example / template of a `nuxt.config.ts` for creating a SPA (Single Page Application) using Nuxt 3:

```typescript
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: "2024-11-01",
    devtools: { enabled: true },
    modules: [
        "@nuxt/icon",
        "@nuxt/fonts",
        "@nuxt/content",
        "@nuxtjs/tailwindcss",
    ],

    app: {
        head: {
            title: "Application Title",
            meta: [
                {
                    name: "description",
                    content: "Application Description",
                },
            ],
            link: [{ rel: "icon", type: "image/png", href: "/logo.png" }],
        },
    },

    imports: {
        dirs: ["stores"],
    },

    typescript: {
        strict: true,
        typeCheck: true,
    },

    ssr: false, // Disable SSR to run as SPA
});
```

When creating a project from scratch, also make sure to include the following dependencies:

-   `vue-tsc`: For TypeScript type checking in Vue files.
-   `@nuxtjs/tailwindcss`: For Tailwind CSS support in Nuxt 3.
-   `prettier`: For code formatting.

# Fetching Data

1. Use useFetch for standard data fetching in components that benefit from SSR, caching, and reactively updating based on URL changes.
2. Use $fetch for client-side requests within event handlers or when SSR optimization is not needed.
3. Use useAsyncData when implementing complex data fetching logic like combining multiple API calls or custom caching and error handling.
4. Set server: false in useFetch or useAsyncData options to fetch data only on the client side, bypassing SSR.
5. Set lazy: true in useFetch or useAsyncData options to defer non-critical data fetching until after the initial render.
6. Custom fetchers can be created using the $fetch API for specific use cases, such as handling authentication tokens or custom headers. These fetchers should be defined in the `plugins/` directory and following the following structure:

```typescript
export default defineNuxtPlugin((nuxtApp) => {
    const token = useACCToken();

    const $accFetch = $fetch.create({
        baseURL: "https://developer.api.autodesk.com",
        onRequest({ request, options }) {
            if (token.value) {
                options.headers.set("Authorization", `Bearer ${token.value}`);
            }
        },
        onResponse({ response }) {},
        onResponseError({ request, response }) {
            if (response.status === 401) {
                token.value = "";
            }
        },
    });

    async function $accFetchPaged<T>(url: string) {
        const items = [] as Array<T>;

        let localUrl = url;

        while (true) {
            const result: any = await $accFetch(localUrl);

            if (result.results) items.push(...result.results);
            if (result.data) items.push(...result.data);

            // If it's the new way
            if (result.pagination?.nextUrl) {
                localUrl = result.pagination.nextUrl;
                continue;
            }

            // If it's the old way
            if (result.links?.next?.href) {
                localUrl = result.links.next.href;
                continue;
            }

            break;
        }

        return items;
    }

    return {
        provide: {
            accFetch: $accFetch,
            accFetchedPaged: $accFetchPaged,
        },
    };
});
```

# UI and Styling

Make sure to use Tailwind for styling components where possible. Additionally also include a `tailwind.config.js` file at the root of the project with the following content:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: "class",
    content: ["packages/**/*.{vue,js,ts}"],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: "#fbffe5",
                    100: "#f3ffc7",
                    200: "#e7ff95",
                    300: "#d4fe58",
                    400: "#bef526",
                    500: "#9fdc06",
                    600: "#84bd00",
                    700: "#5c8506",
                    800: "#4b690b",
                    900: "#3e580f",
                    950: "#1f3201",
                },
            },

            transitionProperty: {
                width: "width",
            },
        },
    },
    plugins: [require("@tailwindcss/container-queries")],
};
```

# Code quality

Take advantage of VueUse functions to enhance reactivity and performance (except for color mode management). Where possible, use TypeScript and make sure to follow valid TypeScript standards.

## SPA Pages

Avoid putting too much logic into the top level `app.vue` component, instead use `layouts/default.vue` and `pages/*.vue` to help break down the logic into it's logical compartments. This will help with readability and maintainability of the code. Example of an `app.vue` file:

```
<template>
    <NuxtErrorBoundary @error="logError">
        <template #default>
            <NuxtLayout>
                <NuxtLoadingIndicator />
                <NuxtPage />
            </NuxtLayout>
        </template>

        <template #error="{ error }">
            <ErrorPage :error="error" />
        </template>
    </NuxtErrorBoundary>
</template>

<script setup lang="ts">
    function logError(error: any) {
        console.error(error);
    }

    // useForgeViewer();
</script>
```

## SPA vs Server

When using Nuxt 3, avoid using the server elements of the framework unless the server is already setup and in use, or the user has specified to use the server. Additionally, the server is required if doing any form of database connection / management. This will help with performance and reduce the amount of code that needs to be maintained. If the user has specified to use the server, make sure to use the server elements of Nuxt 3 to their full potential, including using the server API and server middleware.

## Component Styling

When writing code for component, prefer Composition API `<script setup lang="ts">` style. This will help with readability and maintainability of the code. Additionally, make sure to use the `lang="ts"` attribute to enable TypeScript support in the component. This will help with type checking and improve the overall quality of the code. Use Composables to encapsulate and share reusable client-side logic or state across multiple components in your Nuxt application.

Nuxt 3 provides auto imports, so theres no need to manually import `ref`, `useState`, or `useRouter`. You also don't need to import `defineComponent` or `defineProps` when using `<script setup>`. Additionally do not import any composable functions which are defined in the `composables/` directory, as these are also auto imported.

## Color Mode

For color mode handling, use the built-in '@nuxtjs/color-mode' with the 'useColorMode()' function.

## Naming Conventions

-   Utilize composables, naming them as use<MyComposable>.
-   Use **PascalCase** for component file names (e.g., components/MyComponent.vue).
-   Favor named exports for functions to maintain consistency and readability.
