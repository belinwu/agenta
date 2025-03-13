// @ts-nocheck
import {useCallback, useState, useMemo, useEffect} from "react"

import {MoreOutlined} from "@ant-design/icons"
import {PencilLine, PencilSimple, Trash} from "@phosphor-icons/react"
import {Button, Dropdown, Space, Typography} from "antd"
import dynamic from "next/dynamic"
import {useRouter} from "next/router"
import {createUseStyles} from "react-jss"

import AbTestingEvaluation from "@/oss/components/HumanEvaluations/AbTestingEvaluation"
import SingleModelEvaluation from "@/oss/components/HumanEvaluations/SingleModelEvaluation"
import AutomaticEvalOverview from "@/oss/components/pages/overview/automaticEvaluation/AutomaticEvalOverview"
import DeploymentOverview from "@/oss/components/pages/overview/deployments/DeploymentOverview"
import VariantsOverview from "@/oss/components/pages/overview/variants/VariantsOverview"
import {useAppsData} from "@/oss/contexts/app.context"
import {useAppId} from "@/oss/hooks/useAppId"
import {isDemo} from "@/oss/lib/helpers/utils"
import {useAllVariantsData} from "@/oss/lib/hooks/useAllVariantsData"
import {useVariants} from "@/oss/lib/hooks/useVariants"
import {JSSTheme, Variant} from "@/oss/lib/Types"
import {deleteApp} from "@/oss/services/app-selector/api"
import {useEnvironments} from "@/oss/services/deployment/hooks/useEnvironments"

const CustomWorkflowModal: any = dynamic(
    () => import("@/oss/components/pages/app-management/modals/CustomWorkflowModal"),
)
const CustomWorkflowHistory: any = dynamic(
    () => import("@/oss/components/pages/app-management/drawers/CustomWorkflowHistory"),
)
const ObservabilityOverview: any = dynamic(
    () => import("@/oss/components/pages/overview/observability/ObservabilityOverview"),
)
const DeleteAppModal: any = dynamic(
    () => import("@/oss/components/pages/app-management/modals/DeleteAppModal"),
)
const EditAppModal: any = dynamic(
    () => import("@/oss/components/pages/app-management/modals/EditAppModal"),
)

const {Title} = Typography

const useStyles = createUseStyles((theme: JSSTheme) => ({
    container: {
        display: "flex",
        flexDirection: "column",
        gap: 40,
        "& h1": {
            fontSize: theme.fontSizeHeading4,
            fontWeight: theme.fontWeightMedium,
            lineHeight: theme.lineHeightHeading4,
        },
    },
}))

const OverviewPage = () => {
    const router = useRouter()
    const appId = useAppId()
    const classes = useStyles()
    const {currentApp, mutate: mutateApps} = useAppsData()
    const [isVariantLoading, setIsVariantLoading] = useState(false)
    const [isDeleteAppModalOpen, setIsDeleteAppModalOpen] = useState(false)
    const [isDelAppLoading, setIsDelAppLoading] = useState(false)
    const [isEditAppModalOpen, setIsEditAppModalOpen] = useState(false)
    const [isCustomWorkflowModalOpen, setIsCustomWorkflowModalOpen] = useState(false)
    const {data, mutate: fetchVariants} = useVariants(currentApp)({
        appId: currentApp?.app_id,
    })

    const [isCustomWorkflowHistoryDrawerOpen, setIsCustomWorkflowHistoryDrawerOpen] =
        useState(false)

    const {usernames, data: variants, mutate} = useAllVariantsData({appId})
    const {
        environments,
        isEnvironmentsLoading: isDeploymentLoading,
        mutate: loadEnvironments,
    } = useEnvironments({appId})

    const singleVariant: Variant = useMemo(() => data?.variants?.[0], [data?.variants])

    const [customWorkflowAppValues, setCustomWorkflowAppValues] = useState(() => ({
        appName: "",
        appUrl: "",
        appDesc: "",
    }))

    useEffect(() => {
        if (singleVariant) {
            setCustomWorkflowAppValues({
                appName: currentApp?.app_name ?? "",
                appUrl: singleVariant?.uri ?? "",
                appDesc: "",
            })
        }
    }, [singleVariant, currentApp])

    const handleDeleteOk = useCallback(async () => {
        if (!currentApp) return

        setIsDelAppLoading(true)
        try {
            await deleteApp(currentApp.app_id)
            await mutateApps()
            router.push("/apps")
        } catch (error) {
            console.error(error)
        } finally {
            localStorage.removeItem(`tabIndex_${currentApp.app_id}`)
            setIsDeleteAppModalOpen(false)
            setIsVariantLoading(false)
        }
    }, [currentApp, router])

    return (
        <>
            <div className={classes.container}>
                <Space className="justify-between">
                    <Title>{currentApp?.app_name || ""}</Title>

                    <Dropdown
                        trigger={["click"]}
                        overlayStyle={{width: 180}}
                        menu={{
                            items: [
                                ...(currentApp?.app_type === "custom"
                                    ? [
                                          {
                                              key: "configure",
                                              label: "Configure",
                                              icon: <PencilSimple size={16} />,
                                              onClick: () => setIsCustomWorkflowModalOpen(true),
                                          },
                                          //   {
                                          //       key: "history",
                                          //       label: "History",
                                          //       icon: <ClockCounterClockwise size={16} />,
                                          //       onClick: () =>
                                          //           setIsCustomWorkflowHistoryDrawerOpen(true),
                                          //   },
                                      ]
                                    : [
                                          {
                                              key: "rename_app",
                                              label: "Rename",
                                              icon: <PencilLine size={16} />,
                                              onClick: () => setIsEditAppModalOpen(true),
                                          },
                                      ]),
                                {
                                    key: "delete_app",
                                    label: "Delete",
                                    icon: <Trash size={16} />,
                                    danger: true,
                                    onClick: () => setIsDeleteAppModalOpen(true),
                                },
                            ],
                        }}
                    >
                        <Button type="text" icon={<MoreOutlined />} />
                    </Dropdown>
                </Space>

                <ObservabilityOverview />

                {variants?.length && (
                    <DeploymentOverview
                        variants={variants}
                        isDeploymentLoading={isDeploymentLoading}
                        loadEnvironments={loadEnvironments}
                        environments={environments}
                    />
                )}

                {variants?.length && (
                    <VariantsOverview
                        variantList={variants}
                        isVariantLoading={isVariantLoading}
                        environments={environments}
                        fetchAllVariants={mutate}
                        loadEnvironments={loadEnvironments}
                        usernames={usernames}
                    />
                )}

                {isDemo() && (
                    <>
                        <AutomaticEvalOverview />

                        <AbTestingEvaluation viewType="overview" />

                        <SingleModelEvaluation viewType="overview" />
                    </>
                )}
            </div>
            {currentApp && (
                <DeleteAppModal
                    open={isDeleteAppModalOpen}
                    onOk={handleDeleteOk}
                    onCancel={() => setIsDeleteAppModalOpen(false)}
                    confirmLoading={isDelAppLoading}
                    appDetails={currentApp}
                />
            )}

            {currentApp && (
                <EditAppModal
                    open={isEditAppModalOpen}
                    onCancel={() => setIsEditAppModalOpen(false)}
                    appDetails={currentApp}
                />
            )}

            <CustomWorkflowModal
                open={isCustomWorkflowModalOpen}
                onCancel={() => setIsCustomWorkflowModalOpen(false)}
                customWorkflowAppValues={customWorkflowAppValues}
                setCustomWorkflowAppValues={setCustomWorkflowAppValues}
                handleCreateApp={() => {}}
                configureWorkflow
                fetchVariantsMutate={fetchVariants}
                allVariantsDataMutate={mutate}
                variants={data?.variants}
            />

            <CustomWorkflowHistory
                open={isCustomWorkflowHistoryDrawerOpen}
                onClose={() => setIsCustomWorkflowHistoryDrawerOpen(false)}
            />
        </>
    )
}

export default OverviewPage
