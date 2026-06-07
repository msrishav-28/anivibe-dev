"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { useState, useEffect } from "react";
import { useAuthStore } from "@/store/auth-store";
import { useAuth } from "@clerk/nextjs";
import { setAuthTokenProvider } from "@/lib/api-client";

export function Providers({ children }: { children: React.ReactNode }) {
    const fetchCurrentUser = useAuthStore((state) => state.fetchCurrentUser);
    const { getToken, isLoaded, isSignedIn } = useAuth();

    useEffect(() => {
        setAuthTokenProvider(() => getToken());
        return () => setAuthTokenProvider(null);
    }, [getToken]);

    useEffect(() => {
        if (!isLoaded) return;
        if (isSignedIn) {
            fetchCurrentUser();
        } else {
            useAuthStore.setState({
                user: null,
                isAuthenticated: false,
                isLoading: false,
                error: null,
            });
        }
    }, [fetchCurrentUser, isLoaded, isSignedIn]);

    // Ensure QueryClient is created only once per session on the client
    const [queryClient] = useState(
        () =>
            new QueryClient({
                defaultOptions: {
                    queries: {
                        // With SSR, we usually want to set some default staleTime
                        // above 0 to avoid refetching immediately on the client
                        staleTime: 60 * 1000,
                        refetchOnWindowFocus: false,
                        retry: 1, // Don't retry endlessly if 401
                    },
                },
            })
    );

    return (
        <QueryClientProvider client={queryClient}>
            {children}
            <ReactQueryDevtools initialIsOpen={false} />
        </QueryClientProvider>
    );
}
