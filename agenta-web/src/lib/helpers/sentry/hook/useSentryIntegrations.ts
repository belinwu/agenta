import {useEffect, useRef} from "react"
import {dynamicLib} from "../../dynamic"
import {isDemo} from "../../utils"

export const useSentryIntegrations = () => {
    const isLoading = useRef(false)

    const initilizeSentryIntegrations = async () => {
        const initSentry = await dynamicLib("helpers/sentry/lazyLoadSentryIntegrations")
        initSentry?.lazyLoadSentryIntegrations()
    }

    useEffect(() => {
        if (!isLoading.current && isDemo()) {
            isLoading.current = true

            initilizeSentryIntegrations()
        }
    }, [])
}
