"use client";

import Cookies from "js-cookie";
import { toast } from "sonner";

export type ApiResponse<T> = {
    data: T | null;
    errors?: string;
    status?: number;
};

export async function fetchWithAuth(
    endpoint: string,
    options: RequestInit = {},
    fileUpload: boolean = false
): Promise<Response> {
    // Conditionally retrieve cookies depending on the environment
    const isBrowser = typeof window !== "undefined";
    const auth_token = isBrowser ? Cookies.get("auth_token") : undefined;

    // Log cookies only in the browser environment
    // if (isBrowser) {
    //   console.log("Browser cookies:", document.cookie);
    // }

    const headers = new Headers(options.headers);


    if (!auth_token) {
        toast.error("You need to be logged in to perform this action");
    }

    if (auth_token) {
        headers.set("Authorization", `Bearer ${auth_token}`);
    }

    if (!fileUpload) {
        headers.set("Content-Type", "application/json");
    }

    const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    if (!baseUrl) {
        throw new Error("Base URL is not defined in environment variables");
    }

    return fetch(`${baseUrl}${endpoint}`, {
        ...options,
        headers,
    });
}

export async function handleApiResponse<T>(
    response: Response
): Promise<ApiResponse<T>> {
    const contentType = response.headers.get("content-type");
    let data;

    if (contentType && contentType.includes("application/json")) {
        data = await response.json();
    } else {
        data = await response.text();
    }

    if (!response.ok) {
        return {
            data: null,
            status: response.status,
            errors:
                typeof data === "object" && data.message
                    ? data.message
                    : "An unexpected error occurred",
        };
    }

    return { data, status: response.status };
}

export async function checkauth_token(
    auth_token?: string
): Promise<{ status: number | boolean; data: any }> {
    if (!auth_token) {
        return { status: true, data: "No token found" };
    }

    try {
        const response = await fetchWithAuth("/login", { method: "GET" });
        const data = await response.json();
        if (response.ok) {
            return { status: 0, data }; // Ensure this status is consistent
        }
        if (response.status === 401) {
            return { status: 1, data };
        } else if (response.status === 404) {
            return { status: 2, data };
        }
    } catch (error) {
        console.error("Error validating token:", error);
        return { status: 1, data: error };
    }

    return { status: false, data: "An unexpected error occurred" };
}