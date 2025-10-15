# SPDX-FileCopyrightText: Copyright (C) 2024-2025 沉默の金 <cmzj@cmzj.org>
# SPDX-License-Identifier: GPL-3.0-only
import sys
from importlib.util import find_spec
from pathlib import Path

__author__ = "沉默の金"
__license__ = "GPL-3.0-only"
__copyright__ = "Copyright (C) 2024 沉默の金 <cmzj@cmzj.org>"
name = "LDDC"  # 程序名称(用于common.args检查运行模式)

if find_spec("LDDC") is None:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

# ruff: noqa: E402
from LDDC.common.args import args
from LDDC.common.translator_fastapi import init_translation
from LDDC.common.version import __version__
from LDDC.common.logger_fastapi import get_logger

logger = get_logger()


def main():
    """FastAPI版本的主程序入口"""
    logger.info(f"启动 LDDC v{__version__}")
    
    # 初始化翻译系统
    init_translation("LDDC")
    
    # 根据参数决定运行模式
    if args.get_service_port:
        # 获取服务端口模式
        logger.info("获取服务端口模式")
        # 这里可以实现获取服务端口的逻辑
        print("Service port: 8000")  # 示例端口
        return
    
    # 启动FastAPI服务
    logger.info("启动FastAPI服务模式")
    
    try:
        import uvicorn
        from LDDC.api.main import app
        
        # 配置服务器参数
        host = "127.0.0.1"
        port = 8000
        
        logger.info(f"FastAPI服务将在 http://{host}:{port} 启动")
        
        # 启动服务器
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError:
        logger.error("未找到uvicorn，请安装FastAPI相关依赖")
        sys.exit(1)
    except Exception as e:
        logger.error(f"启动服务时发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()