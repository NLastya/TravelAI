import { useParams } from "react-router-dom";
import style from "./header.module.css";
import { useNavigate } from "react-router-dom";
import {
  Avatar,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
} from "@heroui/react";

const Header = (props) => {
  const { user_id } = useParams();
  const navigate = useNavigate();

  return (
    <div className={style.header}>
      <img src="/icons/logo.svg" alt="logo" onClick={() => navigate("/")} />

      {/* <div className={style.user} onClick={() => {window.location.replace(`/user/${props?.user_id ? props?.user_id : '1'}`)}}>
            <img src='/icons/Ellipse 1.svg' alt='user avatar'/>
            <span>{props?.username ? props?.username : 'Влад З.'}</span>
        </div> */}

      <div className={style.user}>
        <Dropdown placement="bottom-end" disabledKeys={["settings"]}>
          <DropdownTrigger>
            {/* <Avatar
            isBordered
            as="button"
            className="transition-transform"
            src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
          /> */}
            <button className={style.userBtn}>
              <img src="/icons/Ellipse 1.svg" alt="user avatar" />
              <span>{props?.username ? props?.username : "Влад З."}</span>
            </button>
          </DropdownTrigger>
          <DropdownMenu aria-label="Profile Actions" variant="flat">
            <DropdownItem key="personal" href={`/user/${user_id}`}>
              Личный кабинет
            </DropdownItem>
            <DropdownItem key="settings">Настройки</DropdownItem>
            <DropdownItem key="logout" color="danger" href="/auth-in">
              Выйти
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </div>
  );
};

export default Header;
