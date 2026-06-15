export interface TabCaptureRequest {
    browser_tab_id: number;
    title: string;
    url: string;
    favicon?: string;
}