// NewVariantModal.tsx

import React, {useState} from "react"
import {Modal, Input, Select, Space, Typography} from "antd"
import {createUseStyles} from "react-jss"
const {Text} = Typography

interface Props {
    isModalOpen: boolean
    setIsModalOpen: (value: boolean) => void
    addTab: () => void
    variants: any[]
    setNewVariantName: (value: string) => void
    setTemplateVariantName: (value: string) => void
}

const useStyles = createUseStyles({
    select: {
        width: "100%",
    },
})

const NewVariantModal: React.FC<Props> = ({
    isModalOpen,
    setIsModalOpen,
    addTab,
    variants,
    setNewVariantName,
    setTemplateVariantName,
}) => {
    const classes = useStyles()
    const [variantPlaceHolder, setVariantPlaceHolder] = useState("Source Variant")
    const handleTemplateVariantChange = (value: string) => {
        let newValue = value.includes(".") ? value.split(".")[0] : value
        setTemplateVariantName(value)
        setVariantPlaceHolder(`${newValue}`)
    }

    return (
        <Modal
            title="Create a New Variant"
            open={isModalOpen}
            onOk={() => {
                setIsModalOpen(false)
                addTab()
            }}
            onCancel={() => setIsModalOpen(false)}
            centered
        >
            <Space direction="vertical" size={20}>
                <div>
                    <Text>Select an existing variant to use as a template:</Text>
                    <Select
                        className={classes.select}
                        placeholder="Select a variant"
                        onChange={handleTemplateVariantChange}
                        options={variants.map((variant) => ({
                            value: variant.variantName,
                            label: variant.variantName,
                        }))}
                    />
                </div>

                <div>
                    <Text>Enter a unique name for the new variant:</Text>
                    <Input
                        addonBefore={variantPlaceHolder}
                        onChange={(e) => setNewVariantName(e.target.value)}
                    />
                </div>
            </Space>
        </Modal>
    )
}

export default NewVariantModal
