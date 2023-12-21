import React from "react"
import {EvaluatorConfig} from "@/lib/Types"
import {DeleteOutlined, EditOutlined} from "@ant-design/icons"
import {Card, Tag, Typography} from "antd"
import {createUseStyles} from "react-jss"
import Mock from "../evaluationResults/mock"
import dayjs from "dayjs"
import Image from "next/image"
import {useAppTheme} from "@/components/Layout/ThemeContextProvider"

type StyleProps = {
    themeMode: "dark" | "light"
}

const useStyles = createUseStyles({
    body: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    headerRow: {
        display: "flex",
        alignItems: "center",
        alignSelf: "stretch",
        justifyContent: "space-between",
        marginBottom: "1.5rem",
    },
    evaluationImg: ({themeMode}: StyleProps) => ({
        width: 27,
        height: 27,
        marginRight: "8px",
        filter: themeMode === "dark" ? "invert(1)" : "none",
    }),
    name: {
        marginTop: "0.25rem",
        marginBottom: 0,
    },
})

interface Props {
    evaluatorConfig: EvaluatorConfig
}

const EvaluatorCard: React.FC<Props> = ({evaluatorConfig}) => {
    const {appTheme} = useAppTheme()
    const classes = useStyles({themeMode: appTheme} as StyleProps)
    const evaluator = Mock.evaluators.find((item) => item.key === evaluatorConfig.evaluator_key)!

    return (
        <Card actions={[<EditOutlined key="edit" />, <DeleteOutlined key="delete" />]}>
            <div className={classes.body}>
                <div className={classes.headerRow}>
                    <Typography.Text>
                        {dayjs(evaluatorConfig.created_at).format("DD MMM YY")}
                    </Typography.Text>
                    <Tag color={evaluator.color}>{evaluator.name}</Tag>
                </div>

                {evaluator.icon_url && (
                    <Image
                        src={evaluator.icon_url}
                        alt="Exact match"
                        className={classes.evaluationImg}
                    />
                )}

                <Typography.Title className={classes.name} level={4}>
                    {evaluatorConfig.name}
                </Typography.Title>
            </div>
        </Card>
    )
}

export default EvaluatorCard
