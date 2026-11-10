import type { AnchorHTMLAttributes, ReactNode, Ref } from "react";
import {
  Link as RouterLink,
  useLocation,
  useNavigate,
  useParams as useRouterParams,
  useSearchParams as useRouterSearchParams,
} from "react-router";

/**
 * Thin adapter over react-router exposing the `next/link` / `next/navigation`
 * API shape the app was written against, so the Next → Vite migration changed
 * only import specifiers, not component code. New code may use either this or
 * react-router directly — this module is the single place the mapping lives.
 */

type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  /** Destination path — `next/link` calls it `href`; react-router calls it `to`. */
  href: string;
  replace?: boolean;
  children?: ReactNode;
  ref?: Ref<HTMLAnchorElement>;
};

/** Client-side navigation anchor with the `next/link` prop shape. */
export function Link({ href, replace, children, ...rest }: LinkProps) {
  return (
    <RouterLink to={href} replace={replace} {...rest}>
      {children}
    </RouterLink>
  );
}

/** Imperative navigation with the `next/navigation` useRouter() surface. */
export function useRouter() {
  const navigate = useNavigate();
  return {
    push: (href: string) => void navigate(href),
    replace: (href: string) => void navigate(href, { replace: true }),
    back: () => void navigate(-1),
    forward: () => void navigate(1),
  };
}

/** Current pathname (no query string), as `next/navigation`'s usePathname. */
export function usePathname(): string {
  return useLocation().pathname;
}

/** Read-only query params, as `next/navigation`'s useSearchParams. */
export function useSearchParams(): URLSearchParams {
  const [searchParams] = useRouterSearchParams();
  return searchParams;
}

/** Route params typed like `next/navigation`'s useParams. */
export function useParams<T extends Record<string, string>>(): T {
  return useRouterParams() as T;
}
