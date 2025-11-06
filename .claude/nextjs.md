---
name: nextjs
description: Next.js React framework for production. Use for server-side rendering, static site generation, API routes, routing, and full-stack React applications.
---

# Next.js Skill

Comprehensive assistance with Next.js development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

- **Building Next.js applications** - Working with App Router or Pages Router
- **Implementing server components** - Using React Server Components (RSC)
- **Setting up routing** - Creating pages, layouts, or dynamic routes
- **Configuring Turbopack** - Enabling faster builds with `--turbopack` flag
- **Optimizing performance** - Implementing caching, streaming, or data fetching strategies
- **Managing fonts and images** - Using `next/font` or `next/image`
- **Fetching data** - Using `fetch`, `unstable_cache`, or database queries
- **Implementing CSS** - Using Tailwind, CSS Modules, or global styles
- **Debugging Next.js code** - Solving build errors, runtime issues, or configuration problems
- **Upgrading Next.js versions** - Migrating from v12 to v13 or v14 to v15
- **Configuring third-party integrations** - Adding Google Analytics, monitoring tools
- **Working with web vitals** - Implementing performance monitoring with `useReportWebVitals`

## Key Concepts

### App Router vs Pages Router
- **App Router** (v13+): Modern approach using Server Components, supports streaming and nested layouts
- **Pages Router** (legacy): Traditional file-based routing with `pages/` directory

### Server Components vs Client Components
- **Server Components**: Run on server, can access databases directly, reduce client bundle size
- **Client Components**: Run in browser, marked with `'use client'`, have access to hooks and browser APIs

### Rendering Strategies
- **Static Rendering**: Pre-rendered at build time (default for routes without dynamic data)
- **Dynamic Rendering**: Rendered per request when using runtime APIs like `cookies()`, `headers()`
- **Streaming**: Send UI chunks progressively using `<Suspense>` boundaries
- **Partial Prerendering (PPR)**: Mix static and dynamic content in the same route

### Caching Mechanisms
- **Data Cache**: Cache `fetch` responses with `cache: 'force-cache'`
- **Request Memoization**: Deduplicate identical `fetch` calls within same render pass
- **Route Cache**: Pre-rendered HTML stored after build
- **unstable_cache**: Cache database queries and async functions

## Quick Reference

### Common Patterns

**Pattern 1: Basic Data Fetching with fetch**
```javascript
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'force-cache'
  })
  const json = await data.json()
  return <div>{json.title}</div>
}
```

**Pattern 2: Time-Based Revalidation**
```javascript
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // Revalidate every hour
  })
  const json = await data.json()
  return <div>{json.title}</div>
}
```

**Pattern 3: Using Google Fonts**
```typescript
import { Geist } from 'next/font/google'

const geist = Geist({
  subsets: ['latin'],
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Pattern 4: Using Local Fonts**
```typescript
import localFont from 'next/font/local'

const myFont = localFont({
  src: './my-font.woff2',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={myFont.className}>
      <body>{children}</body>
    </html>
  )
}
```

**Pattern 5: Turbopack Configuration**
```javascript
// next.config.js
module.exports = {
  turbopack: {
    resolveAlias: {
      underscore: 'lodash',
    },
    resolveExtensions: ['.mdx', '.tsx', '.ts', '.jsx', '.js', '.json'],
  },
}
```

**Pattern 6: CSS Module Ordering**
```typescript
import utilStyles from './utils.module.css'
import buttonStyles from './button.module.css'

export default function BlogPost() {
  return (
    <div className={utilStyles.container}>
      <button className={buttonStyles.primary}>Click me</button>
    </div>
  )
}
```

**Pattern 7: Installing Tailwind CSS**
```bash
pnpm add -D tailwindcss @tailwindcss/postcss
```

```javascript
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

```css
/* app/globals.css */
@import 'tailwindcss';
```

**Pattern 8: Using unstable_cache for Database Queries**
```typescript
import { unstable_cache } from 'next/cache'
import { getUserById } from '@/app/lib/data'

export default async function Page({ params }: { params: Promise<{ userId: string }> }) {
  const { userId } = await params

  const getCachedUser = unstable_cache(
    async () => getUserById(userId),
    [userId], // Cache key
    { tags: ['user'], revalidate: 3600 }
  )

  const user = await getCachedUser()
  return <div>{user.name}</div>
}
```

**Pattern 9: Using React.use() for Streaming in Client Components**
```typescript
'use client'
import * as React from 'react'

function Page({ params }: { params: Promise<{ id: string }> }) {
  // Unwrap promise in Client Component
  const { id } = React.use(params)
  return <p>ID: {id}</p>
}
```

**Pattern 10: Google Analytics Integration**
```typescript
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XYZ" />
    </html>
  )
}
```

### Example Code Patterns

**Example 1: Async Server Component with await params**
```typescript
async function Page({ params }: { params: Promise<{ id: string }> }) {
  // In Next.js 15+, params is async
  const { id } = await params
  return <p>ID: {id}</p>
}
```

**Example 2: Link Component Migration (v12 → v13)**
```typescript
import Link from 'next/link'

// Next.js 12: `<a>` has to be nested
<Link href="/about">
  <a>About</a>
</Link>

// Next.js 13+: `<Link>` always renders `<a>`
<Link href="/about">
  About
</Link>
```

**Example 3: Revalidating with revalidateTag**
```typescript
// app/lib/data.ts
export async function getUserById(id: string) {
  const data = await fetch(`https://api.example.com/users/${id}`, {
    next: { tags: ['user'] },
  })
  return data.json()
}

// app/lib/actions.ts
import { revalidateTag } from 'next/cache'

export async function updateUser(id: string) {
  // Update user in database...
  revalidateTag('user') // Invalidate all 'user' tagged cache
}
```

**Example 4: Revalidating with revalidatePath**
```typescript
import { revalidatePath } from 'next/cache'

export async function updateProfile(userId: string) {
  // Update user profile in database...
  revalidatePath('/profile') // Revalidate the /profile route
}
```

**Example 5: Web Vitals Monitoring**
```typescript
'use client'
import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    console.log(metric)
    // Send to analytics service
    fetch('/api/analytics', {
      method: 'POST',
      body: JSON.stringify(metric),
    })
  })
  return null
}
```

**Example 6: Template File for Route-Specific Re-mounting**
```typescript
// app/template.tsx
export default function Template({ children }: { children: React.ReactNode }) {
  return <div>{children}</div>
}
```

**Example 7: Streaming with Suspense Boundaries**
```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>My Page</h1>
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>
    </div>
  )
}

async function Posts() {
  const posts = await fetch('https://api.example.com/posts')
  const data = await posts.json()
  return <ul>{data.map(post => <li key={post.id}>{post.title}</li>)}</ul>
}
```

**Example 8: Installing Next.js v13**
```bash
npm i next@13 react@latest react-dom@latest eslint-config-next@13
```

**Example 9: Using Cache Components with Turbopack**
```javascript
// next.config.js
module.exports = {
  experimental: {
    cacheComponents: true, // Enable Cache Components (PPR)
  },
}
```

**Example 10: Generating Trace Files for Performance Debugging**
```bash
NEXT_TURBOPACK_TRACING=1 next dev --turbopack
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **data_fetching.md** - Data Fetching Documentation
Contains detailed information about:
- Dynamic APIs that are now asynchronous in Next.js 15
- How to migrate synchronous API calls to async
- Using `React.use()` to unwrap promises in Client Components
- Codemod tools for automatic migration (`next-async-request-api`)
- Handling `params`, `searchParams`, `cookies()`, `headers()` as promises

**When to use:** When working with dynamic APIs, upgrading to Next.js 15, or encountering "sync-dynamic-apis" warnings.

### **getting_started.md** - Getting Started Documentation (46 pages)
Covers foundational topics including:
- **CSS setup** - Tailwind CSS, CSS Modules, global styles, external stylesheets
- **Caching and Revalidation** - `fetch`, `unstable_cache`, `revalidateTag`, `revalidatePath`
- **Font Optimization** - Using `next/font/google` and `next/font/local`
- **Fetching Data** - Server Components, Client Components, streaming with `use` hook
- **Rendering strategies** - Static, dynamic, streaming, PPR
- **Cache Components** - Fine-grained control with `use cache` directive

**When to use:** When starting a new Next.js project, setting up styling, implementing data fetching, or learning core concepts.

### **other.md** - Other Documentation (30 pages)
Includes miscellaneous topics:
- **Google Analytics integration** - Using `@next/third-parties/google`
- **CI Build Caching** - Optimizing builds in continuous integration
- **Architecture** - How Next.js works under the hood
- **Docs Contribution Guide** - How to contribute to Next.js documentation
- **Fast Refresh** - How Hot Module Replacement works

**When to use:** When integrating third-party services, optimizing CI/CD, understanding Next.js internals, or contributing to the project.

### **routing.md** - Routing Documentation (370 pages)
The largest reference covering:
- **Turbopack** - Faster bundler configuration and migration guide
- **Template files** - `template.js` for route-specific re-mounting behavior
- **Cache Components** - Partial Prerendering (PPR) implementation
- **File conventions** - Special files like `layout.js`, `page.js`, `loading.js`, `error.js`
- **Dynamic routes** - `[slug]`, `[...slug]`, catch-all segments
- **Route handlers** - API routes in App Router
- **Middleware** - Request/response manipulation

**When to use:** When building complex routing logic, configuring Turbopack, implementing layouts/templates, or working with dynamic routes.

## Working with This Skill

### For Beginners
- Start with **getting_started.md** for foundational concepts like CSS setup, fonts, and basic data fetching
- Review the **Quick Reference** section above for common code patterns
- Use **Example Code Patterns** to see how Next.js features work in practice
- Focus on understanding Server Components vs Client Components

### For Intermediate Developers
- Explore **routing.md** for advanced routing patterns, layouts, and templates
- Learn caching strategies from **getting_started.md** (fetch caching, unstable_cache, revalidation)
- Implement **Turbopack** from routing.md for faster builds
- Study **data_fetching.md** to understand async API migration in Next.js 15

### For Advanced Users
- Deep dive into **Cache Components** and **Partial Prerendering (PPR)** in routing.md
- Optimize performance using **streaming**, **Suspense boundaries**, and `use cache`
- Configure **Turbopack** for custom module resolution and webpack loader migration
- Implement **web vitals monitoring** from other.md for production analytics
- Master **revalidation patterns** with `revalidateTag` and `revalidatePath`

### Navigation Tips
- Use the reference file names to quickly locate topics:
  - `data_fetching.md` - Async APIs, promise unwrapping
  - `getting_started.md` - CSS, fonts, caching, basic data fetching
  - `routing.md` - Turbopack, templates, advanced routing
  - `other.md` - Third-party integrations, CI/CD, architecture
- Each reference file includes a **Contents** section at the top for quick navigation
- Code examples include language annotations for better syntax highlighting
- Look for "Good to know" sections for important caveats and tips

## Resources

### references/
Organized documentation extracted from official Next.js docs. These files contain:
- Detailed explanations of Next.js features
- Real-world code examples with language annotations
- Links to original documentation pages
- Table of contents for quick navigation
- "Good to know" tips and warnings

### scripts/
Add helper scripts here for common automation tasks specific to your Next.js projects.

### assets/
Add templates, boilerplate configurations, or example projects here.

## Common Workflows

### Creating a New Next.js App
```bash
npx create-next-app@latest my-app
cd my-app
npm run dev
```

### Adding Tailwind CSS
```bash
pnpm add -D tailwindcss @tailwindcss/postcss
```

Create `postcss.config.mjs` and add `@import 'tailwindcss';` to `app/globals.css` (see Pattern 7).

### Enabling Turbopack for Faster Development
```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build --turbopack"
  }
}
```

### Implementing Caching
- **For fetch calls**: Add `cache: 'force-cache'` option
- **For database queries**: Wrap with `unstable_cache()`
- **For revalidation**: Use `revalidateTag()` or `revalidatePath()`

### Upgrading to Next.js 15
1. Update packages: `npm i next@15 react@latest react-dom@latest`
2. Run codemod: `npx @next/codemod@canary next-async-request-api .`
3. Address async API changes (see data_fetching.md)
4. Test dynamic routes with async `params`

## Troubleshooting

### "Uncached data was accessed outside of <Suspense>" Error
- **Cause**: Dynamic code (e.g., `cookies()`, `headers()`) not wrapped in `<Suspense>`
- **Fix**: Wrap component in `<Suspense fallback={...}>` or use `use cache` directive

### CSS Module Ordering Issues
- **Cause**: Turbopack follows JS import order for CSS modules
- **Fix**: Explicitly use `@import` in CSS or reorder your imports

### Dynamic API Warnings in Next.js 15
- **Cause**: Accessing `params`, `cookies()`, `headers()` synchronously
- **Fix**: `await` the call in Server Components or use `React.use()` in Client Components

### Build Performance Issues
- **Solution**: Enable Turbopack with `next dev --turbopack` and `next build --turbopack`
- **Note**: Build support is in beta as of v15.5.0

## Migration Guides

### Next.js 12 → 13
- Update `<Link>` components to remove nested `<a>` tags
- Migrate `next/image` to new API (run `next-image-to-legacy-image` codemod)
- Update minimum Node.js version to 16.14.0+
- Update React to 18.2.0+

### Next.js 14 → 15
- Dynamic APIs (`params`, `cookies()`, `headers()`) are now async
- Run `npx @next/codemod@canary next-async-request-api .` for automatic migration
- Replace synchronous access with `await` or `React.use()`
- Update route handlers to handle async params

## Version Information

- **Current Documentation Version**: Next.js 15
- **Turbopack Status**: Stable for dev, beta for build (as of v15.5.0)
- **Minimum Node.js Version**: 16.14.0+
- **Minimum React Version**: 18.2.0+

## Notes

- This skill was automatically generated from official Next.js documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information from https://nextjs.org/docs
