import clsx from "clsx"

import usePlayground from "../../hooks/usePlayground"
import {Typography} from "antd"

import type {PlaygroundVariantTestViewProps} from "./types"
import dynamic from "next/dynamic"

const ChatTestView = dynamic(() => import("./Components/ChatTestView"), {ssr: false})
const GenerationTestView = dynamic(() => import("./Components/GenerationTestView"), {ssr: false})

const PlaygroundVariantTestView = ({
    variantId,
    className,
    ...props
}: PlaygroundVariantTestViewProps) => {
    const {isChat} = usePlayground({
        variantId,
        variantSelector: (variant) => {
            return {
                isChat: variant.isChat,
            }
        },
    })
    return (
        <div className={clsx("px-2 w-full", className)} {...props}>
            <div
                className={clsx([
                    "h-[48px] flex items-center gap-4",
                    "border-0 border-b border-solid border-[rgba(5,23,41,0.06)]",
                    "sticky top-0 z-[1]",
                    "bg-white",
                ])}
            >
                <Typography className="text-[14px] leading-[22px] font-[500]">
                    Generation
                </Typography>
            </div>
            {isChat ? (
                <ChatTestView variantId={variantId} />
            ) : (
                <GenerationTestView variantId={variantId} />
            )}
        </div>
    )
}

export default PlaygroundVariantTestView
