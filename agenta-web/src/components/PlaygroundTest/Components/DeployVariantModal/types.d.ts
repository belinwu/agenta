import {Environment, Variant} from "@/lib/Types"
import {ModalProps} from "antd"

export interface Props extends ModalProps {
    variant: Variant
    environments: Environment[]
}
