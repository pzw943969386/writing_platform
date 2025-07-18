import { httpPost } from "@/service/requests";

export const splitText = (data: any = {}) => {
    return httpPost<string>('/tools/split_text', data)
}