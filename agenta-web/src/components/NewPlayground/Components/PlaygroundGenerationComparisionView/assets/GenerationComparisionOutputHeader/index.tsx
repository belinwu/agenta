import {Tag, Typography} from "antd"
import clsx from "clsx"
import {useStyles} from "../styles"
import {GenerationComparisionOutputHeaderProps} from "./types"
import Version from "@/components/NewPlayground/assets/Version"
import usePlayground from "@/components/NewPlayground/hooks/usePlayground"

const GenerationComparisionOutputHeader: React.FC<GenerationComparisionOutputHeaderProps> = ({
    className,
    variantId,
    indexName,
}) => {
    const {variant} = usePlayground({variantId})
    const classes = useStyles()

    return (
        <div className={clsx(classes.title, className)}>
            <Typography>Output {indexName}</Typography>
            <Tag color="default" bordered={false}>
                {variant?.variantName}
            </Tag>
            <Version revision={variant?.revision as number} />
        </div>
    )
}

export default GenerationComparisionOutputHeader
