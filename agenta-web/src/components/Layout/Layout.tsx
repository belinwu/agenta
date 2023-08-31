import React, {useEffect} from "react"
import {Breadcrumb, ConfigProvider, Layout, Space, theme} from "antd"
import Sidebar from "../Sidebar/Sidebar"
import {GithubFilled, LinkedinFilled, TwitterOutlined} from "@ant-design/icons"
import {useRouter} from "next/router"
import Link from "next/link"
import {renameVariablesCapitalizeAll} from "@/lib/helpers/utils"
import {useAppTheme} from "./ThemeContextProvider"
import {useElementSize} from "usehooks-ts"
import {createUseStyles} from "react-jss"
import NoSSRWrapper from "../NoSSRWrapper/NoSSRWrapper"
import {ErrorBoundary} from "react-error-boundary"
import ErrorFallback from "./ErrorFallback"

const {Content, Footer} = Layout

type StyleProps = {
    themeMode: "dark" | "light"
    footerHeight: number
}

const useStyles = createUseStyles({
    layout: ({themeMode}: StyleProps) => ({
        display: "flex",
        background: themeMode === "dark" ? "#141414" : "#ffffff",
        height: "100%",
        minHeight: "100vh",
        position: "relative",
    }),
    content: ({footerHeight}: StyleProps) => ({
        height: `calc(100% - ${footerHeight ?? 0}px)`,
        paddingLeft: "1.5rem",
        paddingRight: "1.5rem",
        marginLeft: 225,
        marginBottom: `calc(2rem + ${footerHeight ?? 0}px)`,
        flex: 1,
    }),
    breadcrumb: {
        padding: "24px 0",
    },
    footer: {
        position: "absolute",
        bottom: 0,
        left: 225,
        right: 0,
        textAlign: "center",
        padding: "5px 20px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
    },
    footerLeft: {
        fontSize: 18,
    },
    footerLinkIcon: ({themeMode}: StyleProps) => ({
        color: themeMode === "dark" ? "#fff" : "#000",
    }),
})

type LayoutProps = {
    children: React.ReactNode
}

const App: React.FC<LayoutProps> = ({children}) => {
    const router = useRouter()
    const {app_name: appName} = router.query
    const {appTheme} = useAppTheme()
    const capitalizedAppName = renameVariablesCapitalizeAll(appName?.toString() || "")
    const [footerRef, {height: footerHeight}] = useElementSize()
    const classes = useStyles({themeMode: appTheme, footerHeight} as StyleProps)

    useEffect(() => {
        const body = document.body
        body.classList.remove("dark-mode", "light-mode")
        if (appTheme === "dark") {
            body.classList.add("dark-mode")
        } else {
            body.classList.add("light-mode")
        }
    }, [appTheme])

    return (
        <NoSSRWrapper>
            {typeof window === "undefined" ? null : (
                <ConfigProvider
                    theme={{
                        algorithm:
                            appTheme === "dark" ? theme.darkAlgorithm : theme.defaultAlgorithm,
                    }}
                >
                    <Layout hasSider className={classes.layout}>
                        <Sidebar />
                        <Content className={classes.content}>
                            <Breadcrumb
                                className={classes.breadcrumb}
                                items={[
                                    {title: <Link href="/apps">Apps</Link>},
                                    {title: capitalizedAppName},
                                ]}
                            />
                            <ErrorBoundary FallbackComponent={ErrorFallback}>
                                {children}
                            </ErrorBoundary>
                        </Content>
                        <Footer ref={footerRef} className={classes.footer}>
                            <Space className={classes.footerLeft} size={10}>
                                <Link href={"https://github.com/Agenta-AI/agenta"} target="_blank">
                                    <GithubFilled className={classes.footerLinkIcon} />
                                </Link>
                                <Link
                                    href={"https://www.linkedin.com/company/agenta-ai/"}
                                    target="_blank"
                                >
                                    <LinkedinFilled className={classes.footerLinkIcon} />
                                </Link>
                                <Link href={"https://twitter.com/agenta_ai"} target="_blank">
                                    <TwitterOutlined className={classes.footerLinkIcon} />
                                </Link>
                            </Space>
                            <div>Copyright © {new Date().getFullYear()} | Agenta.</div>
                        </Footer>
                    </Layout>
                </ConfigProvider>
            )}
        </NoSSRWrapper>
    )
}

export default App
