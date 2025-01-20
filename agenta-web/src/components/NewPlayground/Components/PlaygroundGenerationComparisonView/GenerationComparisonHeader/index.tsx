import {memo, useCallback} from "react"

import clsx from "clsx"
import {Button, Typography} from "antd"
import RunButton from "../../../assets/RunButton"

import usePlayground from "../../../hooks/usePlayground"
import {useStyles} from "./styles"

import {clearRuns} from "../../../hooks/usePlayground/assets/generationHelpers"
import {GenerationComparisonHeaderProps} from "./types"

const GenerationComparisonHeader = ({className}: GenerationComparisonHeaderProps) => {
    const classes = useStyles()
    const {runTests, mutate} = usePlayground()

    const clearGeneration = useCallback(() => {
        mutate(
            (clonedState) => {
                if (!clonedState) return clonedState
                clearRuns(clonedState)
                return clonedState
            },
            {revalidate: false},
        )
    }, [])

    return (
        <section
            className={clsx(
                "flex items-center justify-between gap-2 px-4 py-2 h-[40px]",
                classes.header,
                className,
            )}
        >
            <Typography className={classes.heading}>Generations</Typography>

            <div className="flex items-center gap-2">
                <Button size="small" onClick={clearGeneration}>
                    Clear
                </Button>

                <RunButton type="primary" onClick={() => runTests?.()} />
            </div>
        </section>
    )
}

export default memo(GenerationComparisonHeader)
