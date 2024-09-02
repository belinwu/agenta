import {Evaluator, GenericObject, JSSTheme, Parameter, testset, Variant} from "@/lib/Types"
import {CloseCircleOutlined, CloseOutlined} from "@ant-design/icons"
import {
    ArrowLeft,
    CaretDoubleLeft,
    CaretDoubleRight,
    ClockClockwise,
    Database,
    Lightning,
    Play,
} from "@phosphor-icons/react"
import {
    Button,
    Divider,
    Flex,
    Form,
    Input,
    message,
    Select,
    Space,
    Tag,
    Tooltip,
    Typography,
} from "antd"
import React, {useEffect, useMemo, useRef, useState} from "react"
import {createUseStyles} from "react-jss"
import AdvancedSettings from "./AdvancedSettings"
import {DynamicFormField} from "./DynamicFormField"
import EvaluatorVariantModal from "./EvaluatorVariantModal"
import {
    CreateEvaluationConfigData,
    createEvaluatorConfig,
    updateEvaluatorConfig,
} from "@/services/evaluations/api"
import {useAppId} from "@/hooks/useAppId"
import {useLocalStorage} from "usehooks-ts"
import {getAllVariantParameters} from "@/lib/helpers/variantHelper"
import {randString, removeKeys} from "@/lib/helpers/utils"
import {callVariant} from "@/services/api"

type ConfigureNewEvaluatorProps = {
    setCurrent: React.Dispatch<React.SetStateAction<number>>
    handleOnCancel: () => void
    onSuccess: () => void
    selectedEvaluator: Evaluator
    variants: Variant[] | null
    testsets: testset[] | null
    selectedTestcase: Record<string, any> | null
    setSelectedTestcase: React.Dispatch<React.SetStateAction<Record<string, any> | null>>
    setSelectedVariant: React.Dispatch<React.SetStateAction<Variant | null>>
    selectedVariant: Variant | null
}

const useStyles = createUseStyles((theme: JSSTheme) => ({
    headerText: {
        "& .ant-typography": {
            lineHeight: theme.lineHeightLG,
            fontSize: theme.fontSizeHeading4,
            fontWeight: theme.fontWeightStrong,
        },
    },
    title: {
        fontSize: theme.fontSizeLG,
        fontWeight: theme.fontWeightMedium,
        lineHeight: theme.lineHeightLG,
    },
    formContainer: {
        display: "flex",
        flexDirection: "column",
        gap: theme.padding,
        overflowY: "auto",
        maxHeight: 580,
        "& .ant-form-item": {
            marginBottom: 0,
        },
        "& .ant-form-item-label": {
            paddingBottom: theme.paddingXXS,
        },
    },
    formTitleText: {
        fontSize: theme.fontSize,
        lineHeight: theme.lineHeight,
        fontWeight: theme.fontWeightMedium,
    },
}))

const ConfigureNewEvaluator = ({
    setCurrent,
    selectedEvaluator,
    handleOnCancel,
    variants,
    testsets,
    onSuccess,
    selectedTestcase,
    setSelectedTestcase,
    selectedVariant,
    setSelectedVariant,
}: ConfigureNewEvaluatorProps) => {
    const appId = useAppId()
    const classes = useStyles()
    const [form] = Form.useForm()
    const [debugEvaluator, setDebugEvaluator] = useLocalStorage("isDebugSelectionOpen", false)
    const [openVariantModal, setOpenVariantModal] = useState(false)
    const [submitLoading, setSubmitLoading] = useState(false)
    const [optInputs, setOptInputs] = useState<Parameter[] | null>(null)
    const [optParams, setOptParams] = useState<Parameter[] | null>(null)
    const [isChatVariant, setIsChatVariant] = useState(false)
    const abortControllersRef = useRef<AbortController | null>(null)
    const [isRunningVariant, setIsRunningVariant] = useState(false)

    const evalFields = useMemo(
        () =>
            Object.keys(selectedEvaluator?.settings_template || {})
                .filter((key) => !!selectedEvaluator?.settings_template[key]?.type)
                .map((key) => ({
                    key,
                    ...selectedEvaluator?.settings_template[key]!,
                    advanced: selectedEvaluator?.settings_template[key]?.advanced || false,
                })),
        [selectedEvaluator],
    )

    const advancedSettingsFields = evalFields.filter((field) => field.advanced)
    const basicSettingsFields = evalFields.filter((field) => !field.advanced)

    const onSubmit = (values: CreateEvaluationConfigData) => {
        try {
            setSubmitLoading(true)
            if (!selectedEvaluator.key) throw new Error("No selected key")
            const settingsValues = values.settings_values || {}

            const data = {
                ...values,
                evaluator_key: selectedEvaluator.key,
                settings_values: settingsValues,
            }
            ;(false
                ? updateEvaluatorConfig("initialValues?.id"!, data)
                : createEvaluatorConfig(appId, data)
            )
                .then(onSuccess)
                .catch(console.error)
                .finally(() => setSubmitLoading(false))
        } catch (error: any) {
            setSubmitLoading(false)
            console.error(error)
            message.error(error.message)
        }
    }

    useEffect(() => {
        if (optInputs && selectedTestcase) {
            setSelectedTestcase(() => {
                let result: GenericObject = {}

                optInputs.forEach((data) => {
                    if (selectedTestcase.hasOwnProperty(data.name)) {
                        result[data.name] = selectedTestcase[data.name]
                    }
                })

                result["id"] = randString(6)

                return result
            })
        }
    }, [optInputs])

    useEffect(() => {
        if (!selectedVariant || !selectedTestcase) return

        const fetchParameters = async () => {
            try {
                const {parameters, inputs, isChatVariant} = await getAllVariantParameters(
                    appId,
                    selectedVariant,
                )
                setOptInputs(inputs)
                setOptParams(parameters)
                setIsChatVariant(isChatVariant)
            } catch (error) {
                console.error(error)
            }
        }

        fetchParameters()
    }, [selectedVariant])

    const handleRunVariant = async () => {
        if (!selectedTestcase || !selectedVariant) return
        const controller = new AbortController()
        abortControllersRef.current = controller

        try {
            setIsRunningVariant(true)
            const data = await callVariant(
                isChatVariant ? removeKeys(selectedTestcase, ["chat"]) : selectedTestcase,
                optInputs || [],
                optParams || [],
                appId,
                selectedVariant.baseId,
                isChatVariant ? selectedTestcase.chat || [{}] : [],
                controller.signal,
                true,
            )
            console.log(data)
        } catch (error) {
            console.error(error)
        } finally {
            setIsRunningVariant(false)
        }
    }

    return (
        <div className="flex flex-col gap-6 h-full">
            <div className="flex items-center justify-between">
                <Space className={classes.headerText}>
                    <Button
                        icon={<ArrowLeft size={14} />}
                        className="flex items-center justify-center"
                        onClick={() => setCurrent(1)}
                    />
                    <Typography.Text>Step 2/2:</Typography.Text>
                    <Typography.Text>Configure new evaluator</Typography.Text>
                    <Tag>{selectedEvaluator.name}</Tag>
                </Space>

                <Button onClick={handleOnCancel} type="text" icon={<CloseOutlined />} />
            </div>

            <Flex gap={16} className="h-full">
                <div className="flex-1 flex flex-col gap-4">
                    <div>
                        <Flex justify="space-between">
                            <Typography.Text className={classes.title}>
                                {selectedEvaluator.name}
                            </Typography.Text>
                            <Space>
                                <Button
                                    size="small"
                                    className="flex items-center gap-2"
                                    disabled={true}
                                >
                                    <ClockClockwise />
                                    View history
                                </Button>
                                <Button
                                    size="small"
                                    onClick={() => setDebugEvaluator(!debugEvaluator)}
                                >
                                    {debugEvaluator ? (
                                        <div className="flex items-center gap-2">
                                            Debug
                                            <CaretDoubleRight />
                                        </div>
                                    ) : (
                                        <div className="flex items-center gap-2">
                                            <CaretDoubleLeft />
                                            Debug
                                        </div>
                                    )}
                                </Button>
                            </Space>
                        </Flex>
                        <Typography.Text type="secondary">
                            {selectedEvaluator.description}
                        </Typography.Text>
                    </div>

                    <div className="flex-1">
                        <Form
                            requiredMark={false}
                            form={form}
                            name="new-evaluator"
                            onFinish={onSubmit}
                            layout="vertical"
                            className={classes.formContainer}
                        >
                            <Space direction="vertical" size={4}>
                                <Typography.Text className={classes.formTitleText}>
                                    Identifier
                                </Typography.Text>

                                <div className="flex gap-4">
                                    <Form.Item
                                        name="name"
                                        label="Name"
                                        rules={[
                                            {required: true, message: "This field is required"},
                                        ]}
                                        className="flex-1"
                                    >
                                        <Input />
                                    </Form.Item>
                                    <Form.Item
                                        name="label"
                                        label="Label"
                                        rules={[
                                            {required: true, message: "This field is required"},
                                        ]}
                                        className="flex-1"
                                    >
                                        <Select
                                            mode="multiple"
                                            allowClear
                                            placeholder="Please select"
                                            defaultValue={["item1"]}
                                            options={[
                                                {label: "item1", value: "item1"},
                                                {label: "item2", value: "item2"},
                                            ]}
                                        />
                                    </Form.Item>
                                </div>
                            </Space>

                            {basicSettingsFields.length ? (
                                <Space direction="vertical" size={4}>
                                    <Typography.Text className={classes.formTitleText}>
                                        Parameters
                                    </Typography.Text>
                                    {basicSettingsFields.map((field) => (
                                        <DynamicFormField
                                            {...field}
                                            key={field.key}
                                            name={["settings_values", field.key]}
                                        />
                                    ))}
                                </Space>
                            ) : (
                                ""
                            )}

                            {advancedSettingsFields.length > 0 && (
                                <AdvancedSettings settings={advancedSettingsFields} />
                            )}
                        </Form>
                    </div>

                    <Flex gap={8} justify="end">
                        <Button type="text" onClick={() => form.resetFields()}>
                            Reset
                        </Button>
                        <Button type="primary" loading={submitLoading} onClick={form.submit}>
                            Save configuration
                        </Button>
                    </Flex>
                </div>

                {debugEvaluator && (
                    <>
                        <Divider type="vertical" className="h-full" />

                        <div className="flex-1 flex flex-col gap-4">
                            <Space direction="vertical" size={0}>
                                <Typography.Text className={classes.title}>
                                    Debug evaluator
                                </Typography.Text>
                                <Typography.Text type="secondary">
                                    Test your evaluator by generating a test data
                                </Typography.Text>
                            </Space>

                            <Flex justify="space-between">
                                <Typography.Text className={classes.title}>
                                    Generate test data
                                </Typography.Text>
                                <Space>
                                    <Tooltip
                                        title={testsets?.length === 0 ? "No testset" : ""}
                                        placement="bottom"
                                    >
                                        <Button
                                            size="small"
                                            className="flex items-center gap-2"
                                            onClick={() => setCurrent(3)}
                                            disabled={testsets?.length === 0}
                                        >
                                            <Database />
                                            Load test case
                                        </Button>
                                    </Tooltip>
                                    <Button
                                        size="small"
                                        className="flex items-center gap-2"
                                        onClick={() => setOpenVariantModal(true)}
                                    >
                                        <Lightning />
                                        Select variant
                                    </Button>
                                    {isRunningVariant ? (
                                        <Button
                                            size="small"
                                            danger
                                            onClick={() => {
                                                if (abortControllersRef.current) {
                                                    abortControllersRef.current.abort()
                                                }
                                            }}
                                            type="primary"
                                        >
                                            <CloseCircleOutlined />
                                            Cancel
                                        </Button>
                                    ) : (
                                        <Button
                                            size="small"
                                            className="flex items-center gap-2"
                                            disabled={!selectedTestcase || !selectedVariant}
                                            onClick={handleRunVariant}
                                            loading={isRunningVariant}
                                        >
                                            <Play />
                                            Run variant
                                        </Button>
                                    )}
                                </Space>
                            </Flex>

                            <div className="flex-1 flex flex-col h-full">
                                <Typography.Text className={classes.formTitleText}>
                                    JSON
                                </Typography.Text>
                                <Input.TextArea className="h-full flex-1" placeholder="Textarea" />
                            </div>

                            <div className="flex flex-col gap-2">
                                <Flex justify="space-between">
                                    <Typography.Text className={classes.formTitleText}>
                                        Output
                                    </Typography.Text>
                                    <Button className="flex items-center gap-2" size="small">
                                        <Play /> Run evaluator
                                    </Button>
                                </Flex>

                                <Input.TextArea
                                    className="h-full flex-1"
                                    placeholder="Result"
                                    autoSize={{minRows: 4}}
                                />
                            </div>
                        </div>
                    </>
                )}
            </Flex>

            <EvaluatorVariantModal
                variants={variants}
                open={openVariantModal}
                onCancel={() => setOpenVariantModal(false)}
                setSelectedVariant={setSelectedVariant}
                selectedVariant={selectedVariant}
            />
        </div>
    )
}

export default ConfigureNewEvaluator
