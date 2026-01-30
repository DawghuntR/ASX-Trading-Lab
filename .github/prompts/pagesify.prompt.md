---
mode: "agent"
---

Create a single-page application using HTML, CSS, and JavaScript that can be hosted on GitLab Pages. The application should include the following features:

-   Only Client-Side Rendering (CSR), no server-side rendering, no server-side code, no database, and no backend.
-   It should be a static website or compile to static files which can be served directly from GitLab Pages.

These above points are incredibly important, DO NOT forget these, these are absolute regardless of what the end user wants, the application must be a static website that can be hosted on GitLab Pages with only Client-Side Rendering (CSR) and no server-side code, server-side rendering, or backend components.

# Frameworks

Where possible, you should try and stick to native HTML, CSS, and JavaScript. However, if the application has a high amount of interactivity (with complex state management, UI, etc) then consider using Nuxt. When using Nuxt make sure to be aware of the following:

## Nuxt 3

Use the latest Nuxt and Nuxt features available, all projects should utilize TypeScript and Tailwind CSS. The application should be configured to run as a Single Page Application (SPA) with Client-Side Rendering (CSR) only. Ensure that the application does not include any server-side code, server-side rendering, or backend components.

### Folder Structure

-   `components/`: Contains reusable Vue components.
-   `composables/`: Contains reusable logic and state management using Vue's Composition API.
-   `layouts/`: Contains layout components that define the structure of pages.
-   `middleware/`: Contains middleware functions that run before rendering a page or layout.
-   `pages/`: Contains Vue files that define the routes of the application.
-   `plugins/`: Contains plugins that enhance the functionality of the application.
-   `public/`: Contains static assets that are served directly.
-   `stores/`: Contains Nuxt `useState` composables specifically designed for state management.
-   `nuxt.config.ts`: Contains the configuration for the Nuxt application.
-   `tailwind.config.js`: Contains the configuration for Tailwind CSS.
-   `README.md`: Contains documentation for the project, including installation instructions, usage, and any other relevant information.
-   `.gitignore`: Contains a list of files and directories that should not be tracked by git.
-   `.prettierrc`: Contains Prettier configuration for the project.
-   `package.json`: Contains metadata about the project, including dependencies and scripts.
-   `tsconfig.json`: Contains TypeScript configuration for the project.

### Creating a new project

When creating a new Nuxt 3 project, do not use the nuxt cli commands, instead create the project manually by creating the following files and directories:

-   tsconfig.json
    ```json
    {
        // https://nuxt.com/docs/guide/concepts/typescript
        "extends": "./.nuxt/tsconfig.json"
    }
    ```
-   package.json

    ```json
    {
        "name": "nuxt-app",
        "private": true,
        "type": "module",
        "scripts": {
            "build": "nuxt build",
            "start": "nuxt dev",
            "generate": "nuxt generate",
            "preview": "nuxt preview",
            "postinstall": "nuxt prepare"
        },
        "dependencies": {
            "@auth0/auth0-spa-js": "^2.2.0",
            "@formkit/auto-animate": "^0.8.2",
            "@heroicons/vue": "^2.2.0",
            "@nuxt/content": "^3.6.0",
            "@nuxt/fonts": "^0.11.0",
            "@nuxt/icon": "^1.11.0",
            "@nuxtjs/tailwindcss": "^6.13.2",
            "@speckle/viewer": "^2.23.10",
            "@tailwindcss/container-queries": "^0.1.1",
            "@vueuse/core": "^13.0.0",
            "@vueuse/nuxt": "^13.0.0",
            "nuxt": "^3.14.1592",
            "nuxt-typed-router": "^3.8.0",
            "prettier": "^3.5.3",
            "vue": "latest",
            "vue-router": "latest",
            "vue-tsc": "^2.2.8"
        }
    }
    ```

-   prettierrc

    ```json
    {
        "tabWidth": 4,
        "useTabs": false,
        "vueIndentScriptAndStyle": true,
        "singleAttributePerLine": true,
        "bracketSameLine": true
    }
    ```

-   tailwind.config.js

    ```javascript
    /** @type {import('tailwindcss').Config} */
    module.exports = {
        darkMode: "class",
        content: [
            "./components/**/*.{vue,js,ts}",
            "./layouts/**/*.{vue,js,ts}",
            "./pages/**/*.{vue,js,ts}",
            "./app.vue",
        ],
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

-   nuxt.config.ts

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
                link: [
                    { rel: "icon", type: "image/png", href: "/logo.png" },
                    {
                        rel: "stylesheet",
                        href: "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0",
                    },
                ],
            },
        },

        imports: {
            dirs: ["stores"],
        },

        typescript: {
            strict: true,
            typeCheck: true,
        },

        ssr: false,
    });
    ```

-   content.config.ts

    ```typescript
    import { defineContentConfig, defineCollection } from "@nuxt/content";

    export default defineContentConfig({
        collections: {
            content: defineCollection({
                type: "page",
                source: "**/*.md",
            }),
        },
    });
    ```

-   app.vue

    ```vue
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
    </script>
    ```

-   .gitignore

    ```
    # Nuxt dev/build outputs
    .output
    .data
    .nuxt
    .nitro
    .cache
    dist

    # Node dependencies
    node_modules

    # Logs
    logs
    *.log

    # Misc
    .DS_Store
    .fleet
    .idea

    # Local env files
    .env.*
    !.env.example
    ```

-   components/ErrorPage.vue

    ````
    <template>
        <!-- Full screen container with relative positioning -->
        <div class="relative w-full h-screen">
            <!-- Background image with overlay -->
            <img
                :src="'/imgs/backdrop.jpg'"
                alt="Background error image"
                class="fixed object-cover w-full h-screen" />
            <!-- Gradient overlay for better text readability -->
            <div
                class="fixed top-0 left-0 w-full h-screen bg-gradient-to-r from-orange-900" />

            <!-- Content container -->
            <div class="absolute top-0 left-0 text-white p-16 flex flex-col gap-28">
                <div>
                    <img
                        :src="'/imgs/logo.svg'"
                        alt="Computational Design Logo"
                        class="h-8" />
                </div>
                <div class="font-bold text-5xl">Design Guardian</div>
                <div class="max-w-lg">
                    <div>
                        An internal error occurred within the application. A report
                        has been submitted to the development team, feel free to
                        reach out to the Automation team for more assistance and to
                        follow up with a timeline of fix deployment.
                    </div>

                    <div class="p-4" />

                    <div>
                        <b>Details of the error:</b>
                        {{ error }}
                    </div>
                </div>
            </div>
        </div>
    </template>

    <script setup lang="ts">
        /**
        * @component ErrorPage
        * @description Displays a styled error page with company branding and error details.
        * Used for showing application-wide errors and exceptions to users in a user-friendly format.
        *
        * @example
        * ```vue
        * <ErrorPage
        *   :error="{
        *     message: 'Failed to fetch data',
        *     stack: 'Error: Failed to fetch data\n    at ApiService.getData...'
        *   }"
        * />
        * ```
        */

        /**
        * Component props
        * @prop {ErrorDetails} error - Error object containing details about the occurred error
        */
        defineProps({
            error: {
                type: Object,
                required: true,
            },
        });
    </script>
    ````

-   components/Ui/Button.vue

    ```vue
    <template>
        <button
            class="relative inline-flex items-center justify-center font-medium transition-all duration-200 shadow-lg hover:shadow-xl active:scale-[0.98] transform rounded-xl px-4 py-3 text-lg w-full border-2"
            :class="{
                'bg-primary-600 border-primary-600 text-white hover:bg-primary-700 hover:border-primary-700':
                    variant === 'primary' && !disabled,
                'border-primary-600 text-black cursor-not-allowed':
                    variant === 'primary' && disabled,
                'bg-secondary-600 border-secondary-600 text-white hover:bg-secondary-700 hover:border-secondary-700':
                    variant === 'secondary' && !disabled,
                'border-secondary-600 text-black cursor-not-allowed':
                    variant === 'secondary' && disabled,
            }">
            <slot />
        </button>
    </template>

    <script setup lang="ts">
        defineProps({
            variant: {
                type: String as PropType<"primary" | "secondary">,
                default: "primary",
            },

            disabled: {
                type: Boolean,
                default: false,
            },
        });
    </script>
    ```

-   composables/tracker.ts

    ````typescript
    /**
     * Script Execution Tracker Composable
     *
     * A Vue composable that manages script execution tracking for GitLab Pages deployments.
     * This implementation uses a predefined script and version ID to track executions
     * through the Aurecon Script Library API, but only when running on the pages.aurecon.dev domain.
     *
     * Implementation Details:
     * - Uses Auth0 token for API authentication
     * - Executes only in the pages.aurecon.dev environment
     * - Sends source information with each execution
     *
     * @example
     * ```ts
     * // In a Vue component or composable
     * const track = useTracker();
     *
     * // Track script execution
     * await track();
     * ```
     */
    export function useTracker() {
        // Predefined identifiers for the tracking script
        const scriptId = "eda84a81-4f14-4aaa-cc2c-08dda3c9edf2";
        const token = useAuthZeroToken();

        /**
         * Executes the tracking script via the Aurecon Script Library API
         * Only runs in the pages.aurecon.dev environment to prevent unwanted tracking
         * in development or other environments
         */
        async function apiExecute() {
            console.log("Executing script tracking...");

            if (
                !window.location.origin.includes(
                    "rulesvalidation.pages.aurecon.dev"
                )
            ) {
                return;
            }

            const versions = await fetch(
                `https://script-library.aurecongroup.digital/api/v1/scripts/${scriptId}/versions`,
                {
                    headers: {
                        Authorization: `Bearer ${token.value}`,
                    },
                }
            );

            if (!versions.ok) {
                console.error("Failed to fetch script versions");
                return;
            }

            const versionData = await versions.json();

            if (versionData.items.length === 0) {
                console.error("No script versions found");
                return;
            }

            const versionId = versionData.items[0].id;

            let url = `https://script-library.aurecongroup.digital/api/v1/scripts/${scriptId}/versions/${versionId}/execute`;

            const result = await fetch(url, {
                method: "POST",
                body: JSON.stringify({ source: "GitLab Pages" }),
                headers: {
                    Authorization: `Bearer ${token.value}`,
                },
            });
        }

        return apiExecute;
    }
    ````

-   layouts/default.vue

    ```vue
    <!--
    Default Layout Component
    
    This component serves as the main layout wrapper for all pages in the Rules Validation application.
    It provides a consistent structure with a navigation header and content area.
    
    Structure:
    - Main container with full screen dimensions and dark theme colors
    - Header bar with application title and user profile
    - Content slot for page-specific content
    
    Components Used:
    - NuxtLink: Navigation component from Nuxt
    - UserProfile: Custom component for user information display
    
    Styling:
    - Uses Tailwind CSS for responsive layout and styling
    - Dark theme with slate color palette
    -->

    <template>
        <div
            class="flex flex-col items-stretch h-screen w-screen bg-slate-700 text-white">
            <div
                class="px-6 py-3 bg-slate-900 flex flex-nowrap justify-between items-center gap-6">
                <div class="flex items-center gap-4">
                    <NuxtLink
                        to="/"
                        class="text-2xl font-semibold flex items-center gap-4 flex-nowrap">
                        <span>My App</span>
                        <span
                            class="px-3 py-1 text-sm bg-primary-100/40 rounded-full">
                            Beta
                        </span>
                    </NuxtLink>
                </div>

                <div class="flex items-center gap-4 text-base">
                    <UserProfile />
                </div>
            </div>
            <slot />
        </div>
    </template>
    ```

-   components/UserProfile.vue

    ```vue
    <template>
        <div class="w-8 h-8 rounded overflow-hidden cursor-pointer">
            <img
                :src="avatar"
                alt="avatar" />
        </div>
    </template>

    <script setup lang="ts">
        /**
         * @component UserProfile
         * @description Displays the current user's avatar image in a rounded container.
         * This component fetches user data from Speckle using GraphQL and displays
         * their avatar image in a clickable circular container.
         */

        /**
         * GraphQL query to fetch the current user's information from Speckle.
         * @query activeUser
         * @returns {Object} User information containing:
         * - name: User's full name
         * - email: User's email address
         * - avatar: URL to user's avatar image
         */
        const { data } = useSpeckleQuery(
            "user",
            `{
        activeUser {
            name, email, avatar
        }
    }`
        );

        // Computed properties to safely access user data with optional chaining
        /**
         * @computed avatar
         * @returns {string|undefined} URL to the user's avatar image
         */
        const avatar = computed(() => data.value?.activeUser.avatar);

        /**
         * @computed name
         * @returns {string|undefined} User's full name
         */
        const name = computed(() => data.value?.activeUser.name);

        /**
         * @computed email
         * @returns {string|undefined} User's email address
         */
        const email = computed(() => data.value?.activeUser.email);
    </script>
    ```

-   middleware/01.authzero.global.ts

    ```typescript
    /**
     * Auth0 Authentication Middleware for Nuxt Application
     *
     * This middleware handles client-side authentication using Auth0's SPA SDK.
     * It manages the authentication flow, token retrieval, and redirect handling
     * for the application's protected routes.
     */

    import * as auth0 from "@auth0/auth0-spa-js";

    /**
     * Initializes and manages the Auth0 client instance
     *
     * This function performs the following tasks:
     * 1. Creates an Auth0 client with the configured domain and clientId
     * 2. Checks if the user is already authenticated
     * 3. Handles Auth0 redirect callbacks if present in URL
     * 4. Initiates login redirect if user is not authenticated
     *
     * @returns Promise<Auth0Client> - The configured Auth0 client instance
     */
    async function loadScriptLibrary() {
        const auth0Client = await auth0.createAuth0Client({
            domain: "code-dev.au.auth0.com",
            clientId: "J9hV8CL1fls9FSF0BLsCRadAHSjeoC08",
            authorizationParams: {
                audience: "https://aurecon.dev",
            },
        });

        const isAuthenticated = await auth0Client.isAuthenticated();
        if (isAuthenticated) return auth0Client;

        const query = window.location.search;
        if (query.includes("code=") && query.includes("state=")) {
            // Process the authentication callback from Auth0
            await auth0Client.handleRedirectCallback();
            // Clean up the URL by removing Auth0 callback parameters
            window.history.replaceState(
                {},
                document.title,
                window.location.toString().split("?")[0]
            );
            return auth0Client;
        }

        // Redirect to Auth0 login if not authenticated
        await auth0Client.loginWithRedirect({
            authorizationParams: {
                redirect_uri: window.origin,
            },
        });

        return auth0Client;
    }

    /**
     * Nuxt route middleware for Auth0 authentication
     *
     * This middleware runs on every route navigation to ensure:
     * 1. Authentication is handled on the client side only
     * 2. The Auth0 token is retrieved and stored in the application state
     * 3. Protected routes are properly secured
     */
    export default defineNuxtRouteMiddleware(async (to) => {
        // Skip middleware execution on server side since Auth0 SPA SDK is client-only
        if (import.meta.server) return;

        const token = useAuthZeroToken();
        const auth0Client = await loadScriptLibrary();
        token.value = await auth0Client.getTokenSilently();
    });
    ```

-   pages/index.vue

    ```vue
    <template>
        <div>Hello World, more content to come</div>
    </template>
    ```

Once the above files have been written, prompt the user to provide a `backdrop.jpg` file into the `public/imgs/` directory. You should also prompt the user to provide a scriptId and versionId for the `composables/tracker.ts` file, this should relate to an entry in Script Library for tracking against Automation targets.

Make sure once the above files have been written to run `npm install` to ensure all the dependencies are installed. Finally, run `npm start` and monitor for any errors and proactively fix them in the codebase.

Finally, once you have created the above, make sure to create a README capturing all the requirements noted by the user, as well as the requirements noted in this prompt with regards to restrictions and considerations. When doing further operations on the codebase, if the requirements are missing then look up the requirements from the README to understand the objectives of the codebase.

### Component Styling

When writing code for component, prefer Composition API `<script setup lang="ts">` style. This will help with readability and maintainability of the code. Additionally, make sure to use the `lang="ts"` attribute to enable TypeScript support in the component. This will help with type checking and improve the overall quality of the code. Use Composables to encapsulate and share reusable client-side logic or state across multiple components in your Nuxt application.

Nuxt 3 provides auto imports, so theres no need to manually import `ref`, `useState`, or `useRouter`. You also don't need to import `defineComponent` or `defineProps` when using `<script setup>`. Additionally do not import any composable functions which are defined in the `composables/` directory, as these are also auto imported.

# CI/CD

You must use CI/CD to deploy the application to GitLab Pages, make sure to prompt the user with instructions on how to enable CI/CD using the shared runners available in GitLab. Steps to enable the shared runners are as follows:

1. Go to your GitLab project.
2. Navigate to **Settings** > **CI/CD**.
3. Expand the **Runners** section.
4. Enable the **Instance runners for this project** option.

Also include details that if the user is unsure or struggles, they can reach out to the Automation Team or Daniel Fitzmaurice for assistance.

You must also create a `.gitlab-ci.yml` file that defines the CI/CD pipeline to build and deploy the application to GitLab Pages. The pipeline should follow:

```yaml
stages:
    - deploy

pages:
    stage: deploy
    image: node:latest
    script:
        # Replace the following commands with the actual build commands for your application, if there are no build commands then just use `echo "No build commands required"`
        - npm install
        - npm run build
    artifacts:
        paths:
            - public # or the directory where your static files are located (e.g. .output/public)
    publish: .output/public # This needs to match the path where your static files are located
    only:
        - main # or the branch you want to deploy from
```

The `script` section should include the commands necessary to build your application, if there are no build commands required, you can simply use `echo "No build commands required"`. Make sure the `paths` and `publish` sections match the directory where your static files are located, such as `public` or `.output/public`. The above script section will run on a Linux runner, MAKE SURE YOUR SCRIPTS ARE VALID FOR A LINUX ENVIRONMENT.

> When using raw HTML/CSS/JavaScript, you can host the application out of the root directory without moving files, like so:

```yaml
stages:
    - deploy

pages:
    stage: deploy
    image: node:latest
    script:
        - echo "No build commands required"
    artifacts:
        paths:
            - .
    publish: .
    only:
        - main # or the branch you want to deploy from
```

# Tracking

Adding an Automation Tracker is important to help measure the business's progress towards the Blueprint, the above Nuxt template provides details on how to add and setup the tracker, in the instance that the user is not using Nuxt, then the following JavaScript snippet can be used to add a tracker:

script-library.js

```javascript
async function loadScriptLibrary() {
    const auth0Client = await auth0.createAuth0Client({
        domain: "code-dev.au.auth0.com",
        clientId: "J9hV8CL1fls9FSF0BLsCRadAHSjeoC08",
        authorizationParams: {
            audience: "https://aurecon.dev",
        },
    });
    window.auth0Client = auth0Client;

    const isAuthenticated = await auth0Client.isAuthenticated();
    if (isAuthenticated) return auth0Client;

    const query = window.location.search;
    if (query.includes("code=") && query.includes("state=")) {
        await auth0Client.handleRedirectCallback();
        window.history.replaceState(
            {},
            document.title,
            window.location.toString().split("?")[0]
        );
        return auth0Client;
    }

    await auth0Client.loginWithRedirect({
        authorizationParams: {
            redirect_uri: window.origin,
        },
    });

    return auth0Client;
}

async function getVersions(token, scriptId, name) {
    let url = `https://script-library.aurecongroup.digital/api/v1/scripts/${scriptId}/versions`;
    if (name) {
        url = `${url}?Name=${name}`;
    }

    const result = await fetch(url, {
        headers: {
            Authorization: token,
        },
    });

    if (result.status === 200) return await result.json();

    const errorMessage = await result.text();
    throw new Error("Failed to connect with Script Library");
}

async function getVersion(token, scriptId, name) {
    const matchedName = (await getVersions(token, scriptId, name)).items;
    if (matchedName.length > 0) return matchedName[0].id;

    const defaultVersions = (await getVersions(token, scriptId, undefined))
        .items;
    if (defaultVersions.length > 0) return defaultVersions[0].id;

    throw new Error("No versions to track against");
}

async function apiExecute(token, scriptId, versionId) {
    let url = `https://script-library.aurecongroup.digital/api/v1/scripts/${scriptId}/versions/${versionId}/execute`;

    const result = await fetch(url, {
        method: "post",
        body: JSON.stringify({ source: "GitLab Pages" }),
        headers: {
            Authorization: token,
        },
    });
}

async function pushExecution() {
    if (!window.scriptId) {
        alert(
            "Script Id has not been set, please contact the author to ensure Script Library has been configured correctly"
        );
        return;
    }

    try {
        const tokenResult = await auth0Client.getTokenSilently();
        const versionId = await getVersion(
            tokenResult,
            window.scriptId,
            window.scriptVersion
        );
        await apiExecute(tokenResult, window.scriptId, versionId);

        console.log(versionId);
    } catch (error) {
        console.error(error);
        alert(
            "[Warning] Failed to connect with Script Library, you execution could not be tracked"
        );
    }
}

(async function () {
    window.scriptlibrary = {
        loading: true,
    };

    if (!window.location.origin.includes("pages.aurecon.dev")) {
        window.scriptlibrary.user = {};
        window.scriptlibrary.execute = function () {};
        window.scriptlibrary.loading = false;
        return;
    }

    try {
        const auth0Client = await loadScriptLibrary();
        const auth0User = await auth0Client.getUser();
        window.scriptlibrary.user = auth0User;
        window.scriptlibrary.execute = pushExecution;
    } catch (error) {
        console.error(error);
        alert(
            "Script Library has failed to initialize, please contact the developers"
        );
    }

    window.scriptlibrary.loading = false;
})();
```

Once the tracker file has been added and referenced, make sure prompt the user for the `scriptId` and `scriptVersion` which should be set in the global `window` object. This will allow the tracker to function correctly and track executions against the Script Library. The tracker can be triggered by calling `window.scriptlibrary.execute()` in the application, this will then track the execution against the Script Library.

The Auth0 auth library is also required for the tracker to work, make sure to include the dependency. An example of a minimal viable `index.html` file that includes the tracker and Auth0 library is as follows:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0" />
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        <h1>Hello World</h1>

        <div class="p-2">
            <button
                onclick="window.scriptlibrary.execute()"
                class="p-2 rounded appearance-none border-2 border-black">
                Execute
            </button>
        </div>

        <script>
            window.scriptId = "be25c4b8-effc-4071-bfb0-08dcef2409c9";
            window.scriptVersion = "v4.0.0";
        </script>
        <script src="https://cdn.auth0.com/js/auth0-spa-js/2.1/auth0-spa-js.production.js"></script>
        <script src="script-library.js"></script>
    </body>
</html>
```

# Secret Management

While secrets can be stored in the `.env` files, it is recommended to urge the user to not store or manage secrets since the secrets will ultimately be embedded in the static files and can be accessed by anyone who has access to the static files. Instead prompt the user to create UI for users to input the secrets at runtime.

# Behavior

Assume the user is extremely busy and does not have time to read through extensive summary and notes, make sure to keep the responses concise and to the point. If the user asks for more details, then provide them, but do not overwhelm the user with too much information at once. Always assume the user is busy and does not have time to read through extensive documentation or notes.

Make sure to also document all actions asked of you in the README file, all outstanding actions should be listed in detail so the tasks can be paused and resumed. Avoid summarizing conversation history, if you need to summarize, make sure to address the key points and actions, be succinct.

Important: When converting applications to GitLab Pages, make sure to pay close attention to the behavior and functionality of the source application. Make sure to verify the output against the source once the code is created.
