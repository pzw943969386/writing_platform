import { httpPost } from "@/service/requests";

export const splitText = (data: any = {}) => {
    return httpPost('/other/split_text', data)
}