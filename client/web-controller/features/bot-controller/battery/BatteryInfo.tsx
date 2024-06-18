import { memo, useEffect, useState } from "react";
import { SOCKET_EVENT_NAMES } from "../../../hooks/use-socket";
import { SocketEventBus } from "../../../event-buses/socket.event-bus"
import BatteryChargingFullRoundedIcon from '@mui/icons-material/BatteryChargingFullRounded';

type BatteryInfo = {
    voltage:number;
    percentage:number;
}
export interface IBatteryInfoComponent {
    socketEmit: <T>(event: string, data?: T) => void,
}
const BatteryInfoComponent = (props: IBatteryInfoComponent) => {
    const { socketEmit } = props;
    const [batteryInfo, setBatteryInfo] = useState<BatteryInfo>();

    useEffect(() => {
        const handleSocketMessage = (ev: CustomEvent<MessageEvent>) => {
            const msg = JSON.parse(ev.detail.data ?? '{}');
            if (msg?.event === SOCKET_EVENT_NAMES.BATTERY.BATTERY_INFO) {
                const data = msg.data as BatteryInfo;
                setBatteryInfo(data);
            }
        };
        SocketEventBus.onMessage(handleSocketMessage);


        const requestBatteryInfo = () => {
            socketEmit(SOCKET_EVENT_NAMES.BATTERY.BATTERY_INFO_REQUEST, {});
        }
        const interval = setInterval(() => {
            requestBatteryInfo();
        }, 5000);
        requestBatteryInfo();

        return () => {
            SocketEventBus.offMessage(handleSocketMessage);
            clearInterval(interval);
        }
    }, []);

    return <div style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        padding: "10px",
        textShadow: "1px 1px #646464",
        color: "#ccc",
    }}>
        {!!batteryInfo && <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
        
        }}>
            <BatteryChargingFullRoundedIcon />
            <span>{batteryInfo?.voltage.toFixed(1)}V ({batteryInfo?.percentage.toFixed(0)}%)</span>
        </div>}
    </div>
}

export const BatteryInfo = memo(BatteryInfoComponent);